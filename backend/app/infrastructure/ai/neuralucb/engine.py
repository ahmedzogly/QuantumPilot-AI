"""
NeuralUCB Engine - Core AI Decision Engine
Based on Zhou et al. 2020 NeuralUCB and our context: T1,T2,readout,gate_error,queue,depth,width,algo_type

Context dim = backend(8) + circuit(7) + history(3) = ~18
Action space is discretized: backends x opt_levels x mitigation = e.g. 3 backends * 4 opt * 6 mitigation = 72 arms
But we treat it as contextual bandit where action is chosen via NN that predicts reward per decision
"""
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np
from typing import List, Tuple
import logging

logger = logging.getLogger(__name__)

class RewardNet(nn.Module):
    def __init__(self, context_dim: int = 22, hidden_dim: int = 128):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(context_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1)
        )
        # Xavier init
        for m in self.net:
            if isinstance(m, nn.Linear):
                nn.init.xavier_uniform_(m.weight)
    
    def forward(self, x):
        return self.net(x)

class NeuralUCB:
    def __init__(self, context_dim: int = 22, hidden_dim: int = 128, alpha: float = 1.0, lambda_reg: float = 1.0, lr: float = 1e-3, device="cpu"):
        self.context_dim = context_dim
        self.alpha = alpha
        self.lambda_reg = lambda_reg
        self.device = device
        
        self.model = RewardNet(context_dim, hidden_dim).to(device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        
        # For UCB exploration - covariance matrix
        self.A = lambda_reg * torch.eye(context_dim, device=device)  # Will be updated with grad features
        # Actually for NeuralUCB, A is based on gradients: g(x) g(x)^T
        # We'll maintain A in feature space of last layer gradients
        self.grad_dim = hidden_dim  # approximate
        self.A_grad = lambda_reg * torch.eye(self.grad_dim, device=device)
        self.b = torch.zeros(self.grad_dim, device=device)
        
        self.data_buffer = []  # List of (context, reward)
        self.t = 0
        
    def _get_grad_features(self, context: torch.Tensor) -> torch.Tensor:
        """Get gradient w.r.t last layer as feature for UCB"""
        context = context.unsqueeze(0)
        self.model.zero_grad()
        out = self.model(context)
        out.backward()
        # Get grad of last linear layer
        grad = self.model.net[-1].weight.grad  # [1, hidden]
        return grad.squeeze(0).detach()
    
    def select(self, contexts: List[List[float]]) -> Tuple[int, List[float]]:
        """
        contexts: List of context vectors for each arm (backend+opt+mitigation combo)
        Returns: chosen arm index + UCB scores
        """
        if len(contexts) == 0:
            raise ValueError("No contexts")
        
        if self.t < 10:  # Warmup exploration
            chosen = np.random.choice(len(contexts))
            return chosen, [0.0]*len(contexts)
        
        self.model.eval()
        ucb_scores = []
        with torch.no_grad():
            for ctx in contexts:
                ctx_tensor = torch.tensor(ctx, dtype=torch.float32, device=self.device)
                pred = self.model(ctx_tensor.unsqueeze(0)).item()
                # Compute exploration bonus: sqrt(g^T A^{-1} g)
                # Simplified version using last layer features approximation
                # For production: use exact gradient covariance
                grad_feat = self._get_grad_features(ctx_tensor) if self.model.training else torch.randn(self.grad_dim, device=self.device)*0.1
                try:
                    A_inv = torch.inverse(self.A_grad + 1e-4*torch.eye(self.grad_dim, device=self.device))
                    bonus = self.alpha * torch.sqrt(grad_feat @ A_inv @ grad_feat).item()
                except:
                    bonus = self.alpha * 0.1
                ucb_scores.append(pred + bonus)
        
        chosen = int(np.argmax(ucb_scores))
        logger.info(f"NeuralUCB t={self.t} chosen arm {chosen} scores {ucb_scores}")
        return chosen, ucb_scores
    
    def update(self, context: List[float], reward: float):
        """Online update"""
        self.t += 1
        ctx_tensor = torch.tensor(context, dtype=torch.float32, device=self.device)
        reward_tensor = torch.tensor([reward], dtype=torch.float32, device=self.device)
        
        # Store
        self.data_buffer.append((context, reward))
        
        # Update gradient covariance
        grad_feat = self._get_grad_features(ctx_tensor)
        self.A_grad += torch.outer(grad_feat, grad_feat)
        self.b += reward * grad_feat
        
        # Train model on buffer (mini-batch)
        self.model.train()
        if len(self.data_buffer) >= 16:
            # Sample batch
            batch = self.data_buffer[-32:]
            contexts = torch.tensor([c for c,_ in batch], dtype=torch.float32, device=self.device)
            rewards = torch.tensor([[r] for _,r in batch], dtype=torch.float32, device=self.device)
            
            self.optimizer.zero_grad()
            preds = self.model(contexts)
            loss = self.criterion(preds, rewards)
            loss.backward()
            self.optimizer.step()
            logger.info(f"NeuralUCB update loss={loss.item():.4f} reward={reward:.4f}")
        
        return loss.item() if 'loss' in locals() else 0.0
    
    def build_context(self, circuit_profile, backend_calibration, history_features) -> List[float]:
        """Build full 22-D context vector"""
        backend_ctx = backend_calibration.to_context_vector()  # 8
        circuit_ctx = [
            circuit_profile.num_qubits / 156.0,
            circuit_profile.depth / 500.0,
            circuit_profile.width / 156.0,
            circuit_profile.num_2q_gates / 1000.0,
            circuit_profile.entanglement_ratio,
            1.0 if circuit_profile.algorithm_type=="VQE" else 0.0,
            1.0 if circuit_profile.algorithm_type=="QAOA" else 0.0,
        ]  # 7
        hist = history_features  # e.g. [avg_fidelity_last_10, avg_queue, success_rate] 3
        opt_mit = [0.5, 0.5]  # Placeholder for opt level & mitigation - will be per arm
        # Total ~ 8+7+3+2 =20, pad to 22
        full = backend_ctx + circuit_ctx + hist + opt_mit
        # Pad
        while len(full) < self.context_dim:
            full.append(0.0)
        return full[:self.context_dim]
