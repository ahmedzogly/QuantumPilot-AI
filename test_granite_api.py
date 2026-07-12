import sys
sys.path.insert(0, ".")
from backend.app.infrastructure.ai.granite.client import GraniteClient

client = GraniteClient()
print("Status:", client.get_status())

# Test generate
prompts = [
    "Build a Bell state circuit",
    "Build VQE for H2",
    "Fix this code: from qiskit import QuantumCircuit; qc = QuantumCircuit(2); qc.u1(0.5, 0)"
]

for p in prompts:
    print(f"\n--- Prompt: {p} ---")
    res = client.generate_code(p)
    print(f"Source: {res['source']}")
    print(res['code'][:400])

print("\n=== Mitigation status ===")
from backend.app.infrastructure.ai.mitigation.mitiq_adapter import MitiqAdapter
adapter = MitiqAdapter()
print(adapter.list_available())

print("\n=== Training model exists ===")
import pathlib
print(list(pathlib.Path("models/neuralucb").glob("*.pt")))
