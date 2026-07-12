"""
BackendCalibration - Domain Entity built from real IBM data (fez, marrakesh, kingston) + drift dataset
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

@dataclass
class QubitCalibration:
    qubit: int
    T1_us: float
    T2_us: float
    readout_error: float
    prob_meas0_prep1: float
    prob_meas1_prep0: float
    anharmonicity: Optional[float] = None
    frequency_GHz: Optional[float] = None
    
    @property
    def is_good(self) -> bool:
        # Based on Heron thresholds from live data we fetched
        return self.readout_error < 0.05 and self.T1_us > 30 and self.T2_us > 20

@dataclass
class GateCalibration:
    gate: str
    qubits: List[int]
    gate_error: float
    gate_length_ns: int
    
    @property
    def fidelity(self) -> float:
        return 1.0 - self.gate_error

@dataclass
class BackendCalibration:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    backend_name: str = ""
    num_qubits: int = 0
    last_update: datetime = field(default_factory=datetime.utcnow)
    qubit_calibrations: List[QubitCalibration] = field(default_factory=list)
    gate_calibrations: List[GateCalibration] = field(default_factory=list)
    queue_length: int = 0
    pending_jobs: int = 0
    is_operational: bool = True
    calibration_age_seconds: float = 0
    metadata: Dict = field(default_factory=dict)
    
    # Aggregated features for NeuralUCB context
    @property
    def T1_mean(self) -> float:
        import math
        vals=[q.T1_us for q in self.qubit_calibrations if q.T1_us and not math.isnan(q.T1_us) and not math.isinf(q.T1_us)]
        return sum(vals) / len(vals) if vals else 100.0
    
    @property
    def T2_mean(self) -> float:
        import math
        vals=[q.T2_us for q in self.qubit_calibrations if q.T2_us and not math.isnan(q.T2_us) and not math.isinf(q.T2_us)]
        return sum(vals) / len(vals) if vals else 80.0
    
    @property
    def readout_error_mean(self) -> float:
        import math
        vals=[q.readout_error for q in self.qubit_calibrations if q.readout_error and not math.isnan(q.readout_error)]
        return sum(vals)/len(vals) if vals else 0.02
    
    @property
    def cz_error_mean(self) -> float:
        cz = [g.gate_error for g in self.gate_calibrations if g.gate == 'cz']
        return sum(cz)/len(cz) if cz else 0
    
    @property
    def cz_error_std(self) -> float:
        import numpy as np
        cz = [g.gate_error for g in self.gate_calibrations if g.gate == 'cz']
        return float(np.std(cz)) if cz else 0
    
    def to_context_vector(self) -> List[float]:
        """Core for NeuralUCB - returns backend part of context"""
        return [
            self.T1_mean / 300.0,  # normalized
            self.T2_mean / 300.0,
            self.readout_error_mean * 10,
            self.cz_error_mean * 10,
            self.cz_error_std * 10,
            self.queue_length / 100.0,
            self.pending_jobs / 100.0,
            self.calibration_age_seconds / 3600.0
        ]
