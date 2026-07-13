"""
Drift Transformer with Uncertainty Estimation + Attention Weights Explainability
Shows which time points and which environmental features affected prediction most
For QuantumPilot AI - Explainability as requested: Attention Weights توري أي نقطة زمنية وأي ميزة بيئية أثرت أكتر
"""

import torch
import torch.nn as nn
import math
import numpy as np

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, max_len=5000):
        super().__init__()
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
    def forward(self, x):
        return x + self.pe[:, :x.size(1), :]

class ExplainableTransformerEncoderLayer(nn.Module):
    """Transformer Encoder Layer that returns attention weights for explainability"""
    def __init__(self, d_model=64, nhead=4, dim_feedforward=128, dropout=0.1):
        super().__init__()
        self.self_attn = nn.MultiheadAttention(d_model, nhead, dropout=dropout, batch_first=True)
        self.linear1 = nn.Linear(d_model, dim_feedforward)
        self.dropout = nn.Dropout(dropout)
        self.linear2 = nn.Linear(dim_feedforward, d_model)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)
        
    def forward(self, src, return_attention=False):
        # Self attention with weights
        src2, attn_weights = self.self_attn(src, src, src, need_weights=True, average_attn_weights=False)
        # attn_weights: [batch, nhead, seq, seq] - which time points attended to which
        src = src + self.dropout1(src2)
        src = self.norm1(src)
        src2 = self.linear2(self.dropout(torch.relu(self.linear1(src))))
        src = src + self.dropout2(src2)
        src = self.norm2(src)
        if return_attention:
            return src, attn_weights
        return src

class DriftTransformerExplainable(nn.Module):
    """
    Explainable Drift Transformer with Uncertainty Estimation
    Input: [batch, seq=10, features=8] - T1,T2,kp,neutron,temp,solar,RO,CZ
    Output: predicted T1 + attention weights + feature importance + uncertainty
    """
    def __init__(self, input_dim=8, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super().__init__()
        self.input_dim = input_dim
        self.d_model = d_model
        self.feature_names = ['T1', 'T2', 'Kp', 'Neutron', 'Temp', 'Solar', 'RO', 'CZ'][:input_dim]
        
        self.input_projection = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        
        self.layers = nn.ModuleList([
            ExplainableTransformerEncoderLayer(d_model, nhead, dim_feedforward, dropout)
            for _ in range(num_layers)
        ])
        
        self.fc_out = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )
        
        # Uncertainty estimation: predict both mean and variance (aleatoric uncertainty)
        self.uncertainty_head = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Linear(32, 1),
            nn.Softplus()  # Positive variance
        )
        
    def forward(self, x, return_explainability=False):
        # x: [batch, seq, input_dim]
        batch, seq_len, _ = x.shape
        
        # Input projection
        x_proj = self.input_projection(x)  # [batch, seq, d_model]
        x_proj = self.pos_encoder(x_proj)
        
        # Pass through transformer layers with attention weights
        all_attentions = []
        out = x_proj
        for layer in self.layers:
            out, attn_weights = layer(out, return_attention=True)
            all_attentions.append(attn_weights)  # [batch, nhead, seq, seq]
        
        # Last time step
        last = out[:, -1, :]  # [batch, d_model]
        
        # Predictions
        mean_pred = self.fc_out(last)  # [batch, 1] predicted T1
        variance = self.uncertainty_head(last)  # [batch, 1] uncertainty (variance)
        
        # Feature importance via gradient of output w.r.t input (simple)
        # For explainability: which input features affected prediction most
        # We'll compute via input projection weight magnitudes + gradient
        
        if not return_explainability:
            return mean_pred
        
        # Compute feature importance
        # Method 1: Input projection weight magnitude per feature
        # input_projection weight: [d_model, input_dim] -> importance per feature = mean abs weight
        with torch.no_grad():
            proj_weights = self.input_projection.weight  # [d_model, input_dim]
            feature_importance_proj = proj_weights.abs().mean(dim=0)  # [input_dim]
            
            # Method 2: Attention-based temporal importance
            # Average attention weights over layers, heads, and target positions
            # all_attentions: list of [batch, nhead, seq, seq]
            # We want: for last time step prediction, which past time steps were attended to most?
            # Take last row of attention (query = last position) averaged over heads and layers
            temporal_importance = torch.zeros(batch, seq_len)
            for attn in all_attentions:
                # attn: [batch, nhead, seq, seq]
                # Take attention to last position as query
                last_attn = attn[:, :, -1, :]  # [batch, nhead, seq] - attention from last to all past
                avg_heads = last_attn.mean(dim=1)  # [batch, seq] average over heads
                temporal_importance += avg_heads
            temporal_importance = temporal_importance / len(all_attentions)  # average over layers
            
            # Method 3: Gradient-based feature importance (requires grad)
            # We'll compute gradient of mean_pred w.r.t input x for last step
            # This shows which input features at which time steps influenced prediction most
        
        return {
            "mean": mean_pred,
            "variance": variance,
            "uncertainty": torch.sqrt(variance),  # std dev
            "temporal_importance": temporal_importance,  # [batch, seq] - which time points mattered
            "feature_importance_proj": feature_importance_proj,  # [input_dim] - which features mattered via weights
            "attention_weights": all_attentions,  # list of [batch, nhead, seq, seq] for detailed analysis
            "feature_names": self.feature_names
        }
    
    def explain_prediction(self, x_single):
        """
        Explain single prediction: which time points and which features affected most
        x_single: [seq=10, input_dim=8] single sample
        Returns human-readable explanation
        """
        self.eval()
        x = x_single.unsqueeze(0)  # [1, seq, dim]
        x.requires_grad_(True)
        
        with torch.enable_grad():
            result = self.forward(x, return_explainability=True)
            mean = result["mean"]
            # Compute gradient for feature importance
            mean.backward()
            grad = x.grad  # [1, seq, input_dim] gradient w.r.t input
            # Feature importance = mean absolute gradient over seq and batch
            grad_importance = grad.abs().mean(dim=(0,1))  # [input_dim]
        
        # Get temporal and feature importance
        temporal_imp = result["temporal_importance"][0].detach().cpu().numpy()  # [seq]
        feat_imp_proj = result["feature_importance_proj"].detach().cpu().numpy()  # [input_dim]
        grad_imp = grad_importance.detach().cpu().numpy()  # [input_dim]
        
        # Combine feature importances
        combined_feat_imp = (feat_imp_proj / feat_imp_proj.sum() + grad_imp / (grad_imp.sum()+1e-6)) / 2
        
        # Build explanation
        explanation = {
            "predicted_T1": float(result["mean"].item()),
            "uncertainty_std": float(result["uncertainty"].item()),
            "uncertainty_variance": float(result["variance"].item()),
            "confidence": f"{100*(1 - min(1, result['uncertainty'].item() / (abs(result['mean'].item())+1e-6))):.1f}%",
            "temporal_importance": {
                f"t-{len(temporal_imp)-1-i}": float(temporal_imp[i]) 
                for i in range(len(temporal_imp))
            },
            "most_important_time": f"t-{len(temporal_imp)-1 - int(np.argmax(temporal_imp))} (importance {np.max(temporal_imp):.3f})",
            "feature_importance": {
                name: float(combined_feat_imp[i]) 
                for i, name in enumerate(result["feature_names"])
            },
            "most_important_feature": f"{result['feature_names'][int(np.argmax(combined_feat_imp))]} (importance {np.max(combined_feat_imp):.3f})",
            "attention_weights_shape": [list(a.shape) for a in result["attention_weights"]],
            "interpretation": ""
        }
        
        # Human-readable interpretation
        most_feat = explanation["most_important_feature"]
        most_time = explanation["most_important_time"]
        unc = explanation["uncertainty_std"]
        pred = explanation["predicted_T1"]
        
        explanation["interpretation"] = (
            f"Model predicts future T1 = {pred:.1f}us with uncertainty ±{unc:.1f}us (confidence {explanation['confidence']}). "
            f"Most important feature: {most_feat}. "
            f"Most attended time point: {most_time}. "
            f"For example, if Kp is most important and t-2 is most attended, it means Kp spike 2 steps ago strongly influences future T1 drop - indicating incoming solar storm will affect qubit."
        )
        
        return explanation

# Test
if __name__ == "__main__":
    print("Testing Explainable Drift Transformer with Uncertainty Estimation...")
    model = DriftTransformerExplainable(input_dim=8, d_model=64, nhead=4, num_layers=2)
    
    # Create mock data: 10 time steps, 8 features
    # Simulate: T1 stable 100us, then Kp spike at t-2, T1 drops
    x = torch.randn(1, 10, 8)
    # Make Kp spike at position 7 (t-2 from end)
    x[0, 7, 2] = 5.0  # Kp feature index 2 = 5 (storm)
    
    result = model.forward(x, return_explainability=True)
    print(f"\nPrediction mean: {result['mean'].item():.2f}us, variance: {result['variance'].item():.2f}, uncertainty std: {result['uncertainty'].item():.2f}")
    print(f"Temporal importance shape: {result['temporal_importance'].shape} - Which time points mattered")
    print(f"Feature importance shape: {result['feature_importance_proj'].shape} - Which features mattered via weights")
    print(f"Attention weights: {len(result['attention_weights'])} layers, each {result['attention_weights'][0].shape} [batch, nhead, seq, seq]")
    
    print("\n--- Detailed Explainability ---")
    expl = model.explain_prediction(x[0])
    import json
    print(json.dumps(expl, indent=2))
    
    print("\nExplainable Drift Transformer ready - Shows which time points and which environmental features affected prediction most")
