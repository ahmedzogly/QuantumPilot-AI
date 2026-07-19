"""
Granite Client - HF Inference API version
Uses Qiskit/granite-8b-qiskit via HuggingFace Inference API (0GB local storage)
Instead of loading 16GB model locally, we use API (free tier) or fallback to mock.

This solves the size issue: 8B model = 16GB FP16, Q4_K_M 4.9GB, but API = 0GB.
"""

import os
import logging
from typing import Optional, Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)

class GraniteClient:
    def __init__(self, model_id: str = "Qiskit/granite-8b-qiskit", hf_token: Optional[str] = None):
        self.model_id = model_id
        self.hf_token = hf_token or os.getenv("HF_TOKEN", "")
        self.use_api = True
        self._client = None
        
        # Try to init HF InferenceClient
        try:
            from huggingface_hub import InferenceClient
            if self.hf_token:
                self._client = InferenceClient(model=model_id, token=self.hf_token)
            else:
                # Try without token (public, rate limited)
                self._client = InferenceClient(model=model_id)
            logger.info(f"Granite InferenceClient initialized for {model_id}")
        except Exception as e:
            logger.warning(f"HF InferenceClient not available: {e}, using mock fallback")
            self._client = None
    
    def _mock_generate(self, prompt: str) -> str:
        """Fallback mock when API not available - returns plausible Qiskit code"""
        prompt_lower = prompt.lower()
        if "bell" in prompt_lower or "entangle" in prompt_lower:
            return '''
from qiskit import QuantumCircuit
qc = QuantumCircuit(2,2)
qc.h(0)
qc.cx(0,1)
qc.measure([0,1],[0,1])
print(qc)
'''
        elif "vqe" in prompt_lower or "h2" in prompt_lower:
            return '''
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
theta = Parameter('θ')
qc = QuantumCircuit(2)
qc.ry(theta, 0)
qc.ry(theta, 1)
qc.cx(0,1)
qc.ry(theta, 0)
# VQE for H2 - 2 qubits
print("VQE circuit for H2")
print(qc)
'''
        elif "qaoa" in prompt_lower:
            return '''
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
beta = Parameter('β')
gamma = Parameter('γ')
qc = QuantumCircuit(3)
qc.h(range(3))
qc.rzz(gamma, 0, 1)
qc.rzz(gamma, 1, 2)
qc.rx(beta, range(3))
print(qc)
'''
        else:
            return f'''
from qiskit import QuantumCircuit
# Generated for: {prompt[:100]}
qc = QuantumCircuit(5,5)
qc.h(range(5))
qc.cx(0,1)
qc.cx(1,2)
qc.cx(2,3)
qc.cx(3,4)
qc.measure_all()
print(qc)
# NOTE: Mock fallback - real Granite API would generate better code
'''
    
    def generate_code(self, prompt: str, max_new_tokens: int = 512) -> Dict[str, Any]:
        """
        Generate Qiskit code from natural language prompt
        Uses HF Inference API (0GB) or mock fallback
        """
        if self._client:
            try:
                # HF Inference API format
                # For granite-8b-qiskit, it expects chat template
                from transformers import AutoTokenizer
                # Simplified: direct text generation
                response = self._client.text_generation(
                    prompt=f"User: {prompt}\nAssistant: Provide Qiskit code:",
                    max_new_tokens=max_new_tokens,
                    temperature=0.2,
                    top_p=0.95
                )
                code = response if isinstance(response, str) else str(response)
                return {
                    "code": code,
                    "model": self.model_id,
                    "source": "hf_api",
                    "tokens": len(code.split())
                }
            except Exception as e:
                logger.warning(f"HF API failed: {e}, using mock")
                code = self._mock_generate(prompt)
                return {
                    "code": code,
                    "model": f"{self.model_id} (mock fallback)",
                    "source": "mock",
                    "error": str(e)
                }
        else:
            code = self._mock_generate(prompt)
            return {
                "code": code,
                "model": f"{self.model_id} (mock)",
                "source": "mock"
            }
    
    def fix_code(self, old_code: str) -> Dict[str, Any]:
        """Fix deprecated Qiskit code using Granite knowledge"""
        prompt = f"Fix this deprecated Qiskit code to Qiskit 1.0+ compatible, remove deprecated imports:\n{old_code}"
        return self.generate_code(prompt)
    
    def analyze_circuit_suggestion(self, profile: Dict) -> str:
        """Generate optimization suggestion based on CircuitProfile Q-LEAR features"""
        prompt = f"""
        Circuit Profile: qubits={profile.get('num_qubits')}, depth={profile.get('depth')}, 
        2q_gates={profile.get('num_2q_gates')}, Cw={profile.get('Cw')}, Cd={profile.get('Cd')}, Gc1q={profile.get('Gc1q')}, Gc2q={profile.get('Gc2q')}, Dpe={profile.get('Dpe'):.2f}
        Algorithm: {profile.get('algorithm_type')}
        Backend: T1 mean 135us (ibm_fez) - suggest optimization level and mitigation
        """
        result = self.generate_code(prompt)
        return result["code"]
    
    def get_status(self) -> Dict:
        return {
            "model_id": self.model_id,
            "size_fp16_gb": 16,
            "size_q4_gb": 4.9,
            "local_storage_gb": 0,
            "source": "hf_inference_api",
            "api_available": self._client is not None,
            "fallback": "mock with plausible Qiskit templates",
            "qiskit_humaneval": "46.5% pass@1 (original) / ~44% Q4_K_M",
            "recommendation": "Use API for MVP (0GB), switch to GGUF Q4_K_M 4.9GB with Ollama for production offline"
        }

# Singleton
client = GraniteClient()

if __name__ == "__main__":
    print(client.get_status())
    print("\n--- Test Generation ---")
    tests = [
        "Build a random circuit with 5 qubits",
        "Build a Bell state circuit with 2 qubits",
        "Build VQE for H2 molecule",
        "Build QAOA for MaxCut with 3 nodes"
    ]
    for prompt in tests:
        print(f"\nPrompt: {prompt}")
        res = client.generate_code(prompt)
        print(f"Source: {res['source']} Model: {res['model']}")
        print(res['code'][:500])
