import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error
import json
from pathlib import Path

def generate_near_clifford_circuit(num_qubits: int, depth: int, non_clifford_ratio: float = 0.2):
    qc = QuantumCircuit(num_qubits, num_qubits)
    clifford_gates = ['h','s','sdg','x','cx']
    for _ in range(depth):
        gate = np.random.choice(clifford_gates + ['rz']*2)
        if gate == 'cx' and num_qubits >= 2:
            q0,q1 = np.random.choice(num_qubits, 2, replace=False)
            qc.cx(q0,q1)
        elif gate == 'rz':
            q = np.random.randint(0, num_qubits)
            angle = np.random.uniform(0, 2*np.pi)
            qc.rz(angle, q)
        else:
            q = np.random.randint(0, num_qubits)
            getattr(qc, gate)(q)
    return qc

def generate_training_pair(num_qubits=5, depth=10, noise_model=None):
    qc = generate_near_clifford_circuit(num_qubits, depth)
    qc_meas = qc.copy()
    qc_meas.measure(range(num_qubits), range(num_qubits))
    
    if noise_model is None:
        noise_model = NoiseModel()
        error_2q = depolarizing_error(0.03, 2)
        noise_model.add_all_qubit_quantum_error(error_2q, ['cx','cz'])
        error_1q = depolarizing_error(0.01, 1)
        noise_model.add_all_qubit_quantum_error(error_1q, ['h','x','sx','rz','s'])
    
    ideal_sim = AerSimulator()
    noisy_sim = AerSimulator(noise_model=noise_model)
    
    ideal_result = ideal_sim.run(qc_meas, shots=4096).result()
    noisy_result = noisy_sim.run(qc_meas, shots=4096).result()
    
    return {
        "depth": qc.depth(),
        "num_qubits": num_qubits,
        "ideal_counts": ideal_result.get_counts(),
        "noisy_counts": noisy_result.get_counts(),
    }

if __name__ == "__main__":
    ROOT = Path(__file__).parent.parent
    out_path = ROOT / "datasets" / "clifford_training"
    out_path.mkdir(parents=True, exist_ok=True)
    
    print("Generating 100 near-Clifford training pairs...")
    data = []
    for i in range(100):
        pair = generate_training_pair(num_qubits=np.random.randint(3,8), depth=np.random.randint(5,20))
        data.append(pair)
        if i % 10 == 0:
            print(f"  {i}/100 depth={pair['depth']} ideal={list(pair['ideal_counts'].keys())[:3]}")
    
    with open(out_path / "clifford_training_100.json", "w") as f:
        json.dump(data, f, indent=2)
    
    import pandas as pd
    df = pd.DataFrame([{"depth": d["depth"], "num_qubits": d["num_qubits"], "ideal_counts": str(d["ideal_counts"]), "noisy_counts": str(d["noisy_counts"])} for d in data])
    df.to_parquet(out_path / "clifford_training_100.parquet")
    print(f"Saved to {out_path} {len(data)}")
