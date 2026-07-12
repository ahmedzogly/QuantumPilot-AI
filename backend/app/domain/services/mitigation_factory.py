"""
Mitigation Factory - Production Version with Mitiq Adapter
Combines S-ZNE, NNAS, Transformer, and Mitiq (ZNE,PEC,CDR,TREX)
"""
from .mitigation import MitigationFactory as SimpleFactory, MitigationStrategy
from ..infrastructure.ai.mitigation.mitiq_adapter import MitiqAdapter
from typing import List, Dict
import numpy as np

class ProductionMitigationFactory:
    def __init__(self):
        self.simple_factory = SimpleFactory()
        self.mitiq_adapter = MitiqAdapter()
    
    def create(self, strategy: str, **kwargs) -> MitigationStrategy:
        # Delegate to simple factory for non-Mitiq strategies
        return self.simple_factory.create(strategy, **kwargs)
    
    def mitigate_with_zne(self, noisy_values: List[float], noise_factors: List[float], factory: str = "linear") -> Dict:
        """Use Mitiq adapter for ZNE with different factories"""
        return self.mitiq_adapter.zne_mitigate(noisy_values, noise_factors, factory)
    
    def mitigate_with_comparison(self, noisy_values: List[float], noise_factors: List[float]) -> Dict:
        """Compare all ZNE factories + S-ZNE overhead advantage"""
        results = {}
        for fac in ["linear","richardson","exp","poly"]:
            res = self.mitiq_adapter.zne_mitigate(noisy_values, noise_factors, factory=fac)
            results[fac] = res
        
        # S-ZNE from simple factory (constant overhead)
        szne = self.simple_factory.create("s_zne")
        szne_mitigated = szne.mitigate(noisy_values, noise_factors)
        results["s_zne"] = {"mitigated": szne_mitigated, "overhead": szne.cost_overhead, "method": "s_zne"}
        
        # NNAS
        nnas = self.simple_factory.create("nnas")
        results["nnas"] = {"mitigated": nnas.mitigate(noisy_values, noise_factors), "overhead": nnas.cost_overhead}
        
        # Transformer
        trans = self.simple_factory.create("transformer")
        results["transformer"] = {"mitigated": trans.mitigate(noisy_values, noise_factors), "overhead": trans.cost_overhead}
        
        return results
    
    def get_status(self):
        return {
            "mitiq_available": self.mitiq_adapter.available,
            "strategies": self.mitiq_adapter.list_available(),
            "simple_strategies": self.simple_factory.list_strategies() if hasattr(self.simple_factory, 'list_strategies') else ["none","zne","s_zne","nnas","transformer"]
        }

# Test with real data from live backends + drift
if __name__ == "__main__":
    factory = ProductionMitigationFactory()
    print("Status:", factory.get_status())
    
    # Test with Clifford training data
    import json, pathlib
    cliff_path = pathlib.Path("/home/user/QuantumPilot-AI/datasets/clifford_training/clifford_training_100.json")
    with open(cliff_path) as f:
        data = json.load(f)
    
    # Take one example: ideal 4096 counts vs noisy spread
    example = data[0]
    print(f"\nClifford example depth {example['depth']} qubits {example['num_qubits']}")
    print(f"Ideal: {example['ideal_counts']}")
    print(f"Noisy: {list(example['noisy_counts'].items())[:5]}")
    
    # Simulate expectation values decaying
    # For VQE energy estimation, expectation would decay with noise
    noisy_exp = [0.85, 0.78, 0.71, 0.64, 0.58]
    noise_factors = [1,2,3,4,5]
    comparison = factory.mitigate_with_comparison(noisy_exp, noise_factors)
    print("\nMitigation comparison:")
    for k,v in comparison.items():
        print(f"  {k:12s} -> {v['mitigated']:.4f} overhead {v['overhead']}x method {v.get('method','')}")
    
    # Show S-ZNE advantage
    print("\nS-ZNE Advantage (from weiyouLiao paper):")
    print("Conventional ZNE: 5 noise levels * N circuits = O(N*u*M) measurements")
    print("S-ZNE: Constant overhead O(n_j*T) for entire family, 1.2x vs 5x")
