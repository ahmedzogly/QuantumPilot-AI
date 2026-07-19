"""
Circuit Entity - DDD Aggregate Root
Extended with Q-LEAR features from FSE 2024 paper (8 IBM machines, 25% improvement over QRAFT)
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

@dataclass
class CircuitProfile:
    """Value Object - Circuit analysis result + Q-LEAR features"""
    num_qubits: int
    depth: int
    width: int
    num_2q_gates: int
    num_1q_gates: int
    entanglement_ratio: float
    algorithm_type: str  # VQE, QAOA, Grover, QFT, Custom
    
    # Q-LEAR Features (from paper: https://web-backend.simula.no/sites/default/files/2024-07/3663529.3663830.pdf)
    Cw: int = 0  # Circuit width = total qubits
    Cd: int = 0  # Circuit depth
    Gc1q: int = 0  # Number of single gate ops
    Gc2q: int = 0  # Number of two-qubit gate ops
    Dpe: float = 0.0  # Depth per entanglement? Subcircuit division feature - average depth of subcircuits
    critical_depth: int = 0  # Longest path of 2q gates
    
    # Additional features from NNAS paper for deep circuits
    layerwise_2q_density: List[float] = field(default_factory=list)  # 2q density per layer for NNAS
    estimated_fidelity_proxy: Optional[float] = None
    
    @property
    def is_deep(self) -> bool:
        return self.depth > 100
    
    @property
    def is_wide(self) -> bool:
        return self.num_qubits > 50
    
    @property
    def qlear_feature_vector(self) -> List[float]:
        """Q-LEAR 5-D: Cw, Cd, Gc1q, Gc2q, Dpe"""
        return [float(self.Cw), float(self.Cd), float(self.Gc1q), float(self.Gc2q), float(self.Dpe)]
    
    def to_context_part(self) -> List[float]:
        """7-D circuit part of 22-D context for NeuralUCB"""
        return [
            self.num_qubits / 156.0,
            self.depth / 500.0,
            self.width / 156.0,
            self.num_2q_gates / 1000.0,
            self.entanglement_ratio,
            1.0 if self.algorithm_type=="VQE" else 0.0,
            1.0 if self.algorithm_type=="QAOA" else 0.0,
        ]

@dataclass
class Circuit:
    """Entity - Quantum Circuit - Aggregate Root"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str = ""
    name: str = ""
    qasm: Optional[str] = None
    qiskit_code: Optional[str] = None
    profile: Optional[CircuitProfile] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def update_profile(self, profile: CircuitProfile):
        self.profile = profile
