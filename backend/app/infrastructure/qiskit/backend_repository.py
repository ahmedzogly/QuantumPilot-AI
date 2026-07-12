"""
Backend Repository - Infrastructure implementation
Reuses calibration_drift (8M) + live fetch we did for ibm_fez, marrakesh, kingston
"""
from typing import List, Optional
import pandas as pd
from pathlib import Path
import json
from datetime import datetime

from ...domain.entities.backend_calibration import BackendCalibration, QubitCalibration, GateCalibration

class QiskitBackendRepository:
    def __init__(self, dataset_root: str = "datasets"):
        self.root = Path(dataset_root)
        self.live_files = list((self.root / "calibration_drift").glob("ibm_*_qubits_full.csv"))
    
    def get_live_backends(self) -> List[BackendCalibration]:
        """Load from live CSVs we fetched via QiskitRuntimeService"""
        calibrations = []
        for csv_path in self.live_files:
            backend_name = csv_path.stem.replace("_qubits_full","")
            try:
                df = pd.read_csv(csv_path)
                qubits = []
                for _, row in df.iterrows():
                    qubits.append(QubitCalibration(
                        qubit=int(row['qubit']),
                        T1_us=float(row.get('T1', row.get('T1_us', 100))),
                        T2_us=float(row.get('T2', row.get('T2_us', 80))),
                        readout_error=float(row.get('readout_error', 0.02)),
                        prob_meas0_prep1=float(row.get('prob_meas0_prep1', 0.01)),
                        prob_meas1_prep0=float(row.get('prob_meas1_prep0', 0.01))
                    ))
                # Try to load gates from JSON if exists
                gates = []
                json_path = self.root.parent.parent / f"{backend_name}_properties.json" if (self.root.parent.parent / f"{backend_name}_properties.json").exists() else None
                # For simplicity use empty gates or parse drift_agg
                calibrations.append(BackendCalibration(
                    backend_name=backend_name,
                    num_qubits=len(qubits),
                    last_update=datetime.utcnow(),
                    qubit_calibrations=qubits,
                    gate_calibrations=gates,
                    queue_length=0,
                    pending_jobs=0
                ))
            except Exception as e:
                print(f"Error loading {csv_path}: {e}")
        return calibrations
    
    def get_drift_history(self, backend_name: str = "ibm_fez", limit: int = 1000) -> pd.DataFrame:
        """From phanerozoic dataset 50k sample + agg"""
        drift_path = self.root / "calibration_drift" / "drift_50k.parquet"
        if drift_path.exists():
            import duckdb
            con = duckdb.connect()
            df = con.execute(f"SELECT * FROM parquet_scan('{drift_path}') WHERE backend='{backend_name}' LIMIT {limit}").fetch_df()
            return df
        return pd.DataFrame()
    
    def save_calibration_from_qiskit(self, backend_name: str, properties_dict: dict) -> BackendCalibration:
        """Parse live properties dict (like we fetched from ibm_fez) to domain entity"""
        qubits = []
        for i, q in enumerate(properties_dict.get('qubits', [])):
            rec = {p['name']: p['value'] for p in q}
            qubits.append(QubitCalibration(
                qubit=i,
                T1_us=rec.get('T1', 100) * 1e6 if rec.get('T1', 0) < 0.01 else rec.get('T1', 100),
                T2_us=rec.get('T2', 80) * 1e6 if rec.get('T2', 0) < 0.01 else rec.get('T2', 80),
                readout_error=rec.get('readout_error', 0.02),
                prob_meas0_prep1=rec.get('prob_meas0_prep1', 0.01),
                prob_meas1_prep0=rec.get('prob_meas1_prep0', 0.01)
            ))
        gates = []
        for g in properties_dict.get('gates', [])[:500]:
            params = {p['name']: p['value'] for p in g['parameters']}
            gates.append(GateCalibration(
                gate=g['gate'],
                qubits=g['qubits'],
                gate_error=params.get('gate_error', 0.01),
                gate_length_ns=params.get('gate_length', 100)
            ))
        return BackendCalibration(
            backend_name=backend_name,
            num_qubits=len(qubits),
            last_update=datetime.utcnow(),
            qubit_calibrations=qubits,
            gate_calibrations=gates
        )
