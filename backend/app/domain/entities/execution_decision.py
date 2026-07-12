"""
ExecutionDecision - DDD Aggregate Root - Output of NeuralUCB
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import uuid
from enum import Enum

class OptimizationLevel(int, Enum):
    LEVEL_0 = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3

class MitigationStrategy(str, Enum):
    NONE = "none"
    ZNE = "zne"
    S_ZNE = "s_zne"  # From weiyouLiao paper
    TREX = "trex"
    PEC = "pec"
    CDR = "cdr"
    AVPP = "avpp"  # From Kaggle dataset
    NOISE_AGNOSTIC = "noise_agnostic"  # From Nature paper 2025

class ResilienceLevel(int, Enum):
    L0 = 0
    L1 = 1
    L2 = 2

@dataclass
class ExecutionDecision:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    circuit_id: str = ""
    backend_name: str = ""
    optimization_level: OptimizationLevel = OptimizationLevel.LEVEL_2
    mitigation_strategy: MitigationStrategy = MitigationStrategy.S_ZNE
    resilience_level: ResilienceLevel = ResilienceLevel.L1
    shots: int = 4096
    expected_fidelity: float = 0.0
    expected_cost_seconds: float = 0.0
    expected_queue_seconds: float = 0.0
    confidence: float = 0.0  # UCB exploration bonus
    context_vector: List[float] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    def is_high_confidence(self) -> bool:
        return self.confidence > 0.8

@dataclass
class ExecutionResult:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    decision_id: str = ""
    backend_name: str = ""
    success: bool = False
    fidelity: Optional[float] = None
    hellinger_fidelity: Optional[float] = None
    execution_time_ms: int = 0
    queue_time_ms: int = 0
    cost_seconds: float = 0
    counts: Optional[dict] = None
    error_message: Optional[str] = None
    mitigation_applied: bool = False
    created_at: datetime = field(default_factory=datetime.utcnow)
    
    @property
    def reward(self) -> float:
        """Multi-objective reward for NeuralUCB"""
        if not self.success:
            return -1.0
        # w1=0.5 fidelity, w2=0.2 time, w3=0.2 queue, w4=0.1 cost
        fidelity_term = (self.fidelity or 0) * 0.5
        time_penalty = (self.execution_time_ms / 10000) * 0.2
        queue_penalty = (self.queue_time_ms / 60000) * 0.2
        cost_penalty = (self.cost_seconds / 600) * 0.1
        return fidelity_term - time_penalty - queue_penalty - cost_penalty
