"""
Circuit Analyzer Use Case - Clean Architecture
Extended with Q-LEAR + NNAS features
"""
from typing import Dict, List
from qiskit import QuantumCircuit
from qiskit.converters import circuit_to_dag
from ...domain.entities.circuit import CircuitProfile

class CircuitAnalyzer:
    def analyze_qasm(self, qasm_str: str) -> CircuitProfile:
        try:
            # Try QASM3 then QASM2
            qc = QuantumCircuit.from_qasm_str(qasm_str)
        except:
            from qiskit.qasm3 import loads
            qc = loads(qasm_str)
        return self._from_qiskit(qc, algorithm_type="Custom")
    
    def analyze_qiskit_code(self, code: str) -> CircuitProfile:
        # For MVP, placeholder - in production use granite-8b-qiskit to generate standardized code
        # TODO: integrate granite model
        return CircuitProfile(
            num_qubits=5,
            depth=10,
            width=5,
            num_2q_gates=10,
            num_1q_gates=20,
            entanglement_ratio=0.5,
            algorithm_type="Custom",
            Cw=5, Cd=10, Gc1q=20, Gc2q=10, Dpe=5.0
        )
    
    def _from_qiskit(self, qc: QuantumCircuit, algorithm_type: str = "Custom") -> CircuitProfile:
        depth = qc.depth()
        width = qc.num_qubits
        ops = qc.count_ops()
        num_2q = sum(v for k,v in ops.items() if k in ['cx','cz','ecr','rzz','crx','cry','cp'])
        num_1q = sum(v for k,v in ops.items() if k in ['x','sx','rz','rx','ry','h','s','t','id','u','u1','u2','u3'])
        
        entanglement_ratio = num_2q / (num_1q + num_2q + 1e-6)
        
        # Q-LEAR features
        Cw = width
        Cd = depth
        Gc1q = num_1q
        Gc2q = num_2q
        
        # Dpe: divide transpiled circuit into subcircuits for depth per entanglement
        # Simplified: average depth per 2q gate layer
        try:
            dag = circuit_to_dag(qc)
            layers = list(dag.layers())
            # Count layers containing 2q
            layers_with_2q = sum(1 for layer in layers if any(len(op.qargs)==2 for op in layer['graph'].op_nodes()))
            Dpe = depth / (layers_with_2q + 1e-6)
            # Layerwise 2q density for NNAS paper
            layerwise_density = []
            for layer in layers:
                ops_in_layer = list(layer['graph'].op_nodes())
                two_q = sum(1 for op in ops_in_layer if len(op.qargs)==2)
                density = two_q / (len(ops_in_layer)+1e-6)
                layerwise_density.append(float(density))
            critical_depth = layers_with_2q
        except Exception as e:
            Dpe = float(depth) / (num_2q + 1)
            layerwise_density = [entanglement_ratio]*depth
            critical_depth = num_2q
        
        # Fidelity proxy: product of gate fidelities using live data avg 0.99 for 1q, 0.97 for 2q
        fidelity_proxy = (0.99 ** num_1q) * (0.97 ** num_2q)
        
        return CircuitProfile(
            num_qubits=width,
            depth=depth,
            width=width,
            num_2q_gates=num_2q,
            num_1q_gates=num_1q,
            entanglement_ratio=entanglement_ratio,
            algorithm_type=algorithm_type,
            Cw=Cw,
            Cd=Cd,
            Gc1q=Gc1q,
            Gc2q=Gc2q,
            Dpe=Dpe,
            critical_depth=critical_depth,
            layerwise_2q_density=layerwise_density[:20],  # first 20 layers
            estimated_fidelity_proxy=fidelity_proxy
        )

# Quick test
if __name__ == "__main__":
    from qiskit import QuantumCircuit
    qc = QuantumCircuit(3)
    qc.h(0)
    qc.cx(0,1)
    qc.cx(1,2)
    qc.rz(0.5, 0)
    analyzer = CircuitAnalyzer()
    p = analyzer._from_qiskit(qc, "VQE")
    print(p)
    print("Q-LEAR vector:", p.qlear_feature_vector)
