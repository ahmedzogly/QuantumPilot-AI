import sys
sys.path.insert(0, ".")
from backend.app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)
print("=== Testing QuantumPilot API ===")
print(client.get("/").json())
print(client.get("/api/v1/health").json())
print("\nBackends:")
resp = client.get("/api/v1/backends")
print(resp.json())

print("\nAnalyze:")
resp = client.post("/api/v1/analyze", json={"name":"test Bell","qasm":"OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[3] q;\nh q[0];\ncx q[0], q[1];\n","algorithm_type":"VQE"})
print(resp.json())

print("\nDecide:")
resp = client.post("/api/v1/decide", json={"name":"test","qasm":"OPENQASM 3.0;\ninclude \"stdgates.inc\";\nqubit[3] q;\nh q[0];\ncx q[0], q[1];\n","algorithm_type":"VQE"})
print(resp.json())
