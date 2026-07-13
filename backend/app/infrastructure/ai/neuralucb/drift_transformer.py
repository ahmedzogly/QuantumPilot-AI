"""
Drift Transformer - Time-Series Forecasting for T1/T2 - Strengthening LSTM
For QuantumPilot AI - Integrated with NeuralUCB (Don't replace, combine)
"""

import torch
import torch.nn as nn
import math

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

class DriftTransformer(nn.Module):
    def __init__(self, input_dim=8, d_model=64, nhead=4, num_layers=2, dim_feedforward=128, dropout=0.1):
        super().__init__()
        self.input_dim = input_dim
        self.d_model = d_model
        self.input_projection = nn.Linear(input_dim, d_model)
        self.pos_encoder = PositionalEncoding(d_model)
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model,
            nhead=nhead,
            dim_feedforward=dim_feedforward,
            dropout=dropout,
            batch_first=True
        )
        self.transformer_encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.fc_out = nn.Sequential(
            nn.Linear(d_model, 32),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(32, 1)
        )
        
    def forward(self, x):
        x = self.input_projection(x)
        x = self.pos_encoder(x)
        encoded = self.transformer_encoder(x)
        last = encoded[:, -1, :]
        output = self.fc_out(last)
        return output

class DriftPredictorEnsemble(nn.Module):
    def __init__(self, input_dim=1, lstm_hidden=32, transformer_d_model=64):
        super().__init__()
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=lstm_hidden, batch_first=True)
        self.lstm_fc = nn.Linear(lstm_hidden, 1)
        self.transformer = DriftTransformer(input_dim=input_dim, d_model=transformer_d_model)
        self.ensemble_weight = nn.Parameter(torch.tensor([0.5, 0.5]))
        
    def forward(self, x_lstm, x_transformer):
        lstm_out, _ = self.lstm(x_lstm)
        lstm_pred = self.lstm_fc(lstm_out[:, -1, :])
        trans_pred = self.transformer(x_transformer)
        weights = torch.softmax(self.ensemble_weight, dim=0)
        ensemble = weights[0] * lstm_pred + weights[1] * trans_pred
        return {
            "lstm": lstm_pred,
            "transformer": trans_pred,
            "ensemble": ensemble,
            "weights": weights
        }

if __name__ == "__main__":
    print("Testing DriftTransformer...")
    model = DriftTransformer(input_dim=8, d_model=64, nhead=4, num_layers=2)
    x = torch.randn(4, 10, 8)
    out = model(x)
    print(f"Input {x.shape} -> Output {out.shape} (future T1)")
    print("\nTesting Ensemble...")
    ensemble = DriftPredictorEnsemble(input_dim=8)
    x_lstm = torch.randn(4, 10, 1)
    x_trans = torch.randn(4, 10, 8)
    res = ensemble(x_lstm, x_trans)
    print(f"LSTM {res['lstm'].shape}, Transformer {res['transformer'].shape}, Ensemble {res['ensemble'].shape}, Weights {res['weights']}")
    print("DriftTransformer ready - Strengthening LSTM, not replacing NeuralUCB")
