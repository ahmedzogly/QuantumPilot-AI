import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function CircuitInput({ onAnalyze }) {
  const { t, locale } = useLanguage()
  const [activeTab, setActiveTab] = useState('qasm')
  const [qasm, setQasm] = useState(`OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;
bit[3] c;
h q[0];
cx q[0], q[1];
cx q[1], q[2];
c[0] = measure q[0];
c[1] = measure q[1];
c[2] = measure q[2];`)
  
  const [qiskitCode, setQiskitCode] = useState(`from qiskit import QuantumCircuit

qc = QuantumCircuit(3, 3)
qc.h(0)
qc.cx(0, 1)
qc.cx(1, 2)
qc.measure([0,1,2], [0,1,2])

print(qc)
print(f"Depth: {qc.depth()}, Qubits: {qc.num_qubits}")`)

  const [algoType, setAlgoType] = useState('VQE')
  const [analyzing, setAnalyzing] = useState(false)
  const [profile, setProfile] = useState(null)

  const examples = {
    Bell_QASM: `OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
h q[0];
cx q[0], q[1];
c = measure q;`,
    Bell_Qiskit: `from qiskit import QuantumCircuit

qc = QuantumCircuit(2, 2)
qc.h(0)
qc.cx(0, 1)
qc.measure([0, 1], [0, 1])
print("Bell State")
print(qc)`,
    VQE_H2_QASM: `OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
ry(1.0) q[0];
ry(1.0) q[1];
cx q[0], q[1];
ry(0.5) q[0];
c = measure q;`,
    VQE_H2_Qiskit: `from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

theta = Parameter('θ')
qc = QuantumCircuit(2, 2)
qc.ry(theta, 0)
qc.ry(theta, 1)
qc.cx(0, 1)
qc.ry(theta, 0)
qc.measure_all()

print("VQE for H2 - 2 qubits")
print(qc)
print(f"Parameters: {qc.parameters}")`,
    QAOA_QASM: `OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;
bit[3] c;
h q[0]; h q[1]; h q[2];
rzz(0.5) q[0], q[1];
rzz(0.5) q[1], q[2];
rx(0.3) q;
c = measure q;`,
    QAOA_Qiskit: `from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

beta = Parameter('β')
gamma = Parameter('γ')

qc = QuantumCircuit(3, 3)
qc.h(range(3))
qc.rzz(gamma, 0, 1)
qc.rzz(gamma, 1, 2)
qc.rx(beta, range(3))
qc.measure_all()

print("QAOA for MaxCut 3 nodes")
print(qc)`
  }

  const handleAnalyze = async () => {
    setAnalyzing(true)
    try {
      const code = activeTab === 'qasm' ? qasm : qiskitCode
      const lines = code.split('\n').length
      const hasCX = (code.match(/cx|CX|cnot/i) || []).length
      const hasH = (code.match(/\bh\b|H\(/) || []).length
      const numQubitsMatch = activeTab === 'qasm' 
        ? code.match(/qubit\[(\d+)\]/) 
        : code.match(/QuantumCircuit\((\d+)/)
      const numQubits = numQubitsMatch ? parseInt(numQubitsMatch[1]) : 3
      
      const mockProfile = {
        num_qubits: numQubits,
        depth: lines,
        width: numQubits,
        num_2q_gates: hasCX,
        num_1q_gates: hasH + 5,
        entanglement_ratio: hasCX / (hasH + hasCX + 1),
        algorithm_type: algoType,
        Cw: numQubits,
        Cd: lines,
        Gc1q: hasH + 5,
        Gc2q: hasCX,
        Dpe: lines / (hasCX + 1),
        estimated_fidelity_proxy: 0.85 + (numQubits * 0.02),
        language: activeTab
      }
      setProfile(mockProfile)
      if (onAnalyze) onAnalyze(mockProfile, code)
    } catch (e) {
      console.error(e)
    }
    setAnalyzing(false)
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (ev) => {
        const content = ev.target.result
        if (content.includes('QuantumCircuit') || content.includes('from qiskit') || content.includes('import qiskit')) {
          setActiveTab('qiskit')
          setQiskitCode(content)
        } else {
          setActiveTab('qasm')
          setQasm(content)
        }
      }
      reader.readAsText(file)
    }
  }

  return (
    <div>
      <div style={{ marginBottom: 16, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <div>
          <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>
            {locale === 'ar' ? 'إدخال الدائرة الكمومية' : 'Quantum Circuit Input'}
          </h3>
          <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>
            {locale === 'ar' ? 'أين يدخل الباحث دائرته - QASM 3.0 أو Qiskit Python + توليد بالذكاء الاصطناعي' : 'Where researcher enters circuit - QASM 3.0 or Qiskit Python + AI generation'}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
          <select value={algoType} onChange={e=>setAlgoType(e.target.value)} style={{ padding: '6px 10px', background: '#0f111a', color: '#c6c6c6', border: '1px solid #1e2235', borderRadius: 6, fontSize: 12 }}>
            <option value="VQE">VQE</option>
            <option value="QAOA">QAOA</option>
            <option value="Grover">Grover</option>
            <option value="QFT">QFT</option>
            <option value="Custom">Custom</option>
          </select>
          <label style={{ fontSize: 11, padding: '6px 12px', borderRadius: 6, background: '#0f62fe', color: 'white', border: '1px solid #0f62fe', cursor: 'pointer' }}>
            {locale==='ar' ? 'رفع ملف' : 'Upload'}
            <input type="file" accept=".qasm,.qpy,.py,.txt" onChange={handleFileUpload} style={{ display: 'none' }} />
          </label>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 8, marginBottom: 12 }}>
        <button
          onClick={()=>setActiveTab('qasm')}
          style={{
            padding: '6px 14px',
            background: activeTab==='qasm' ? '#0f62fe' : '#1a1a2e',
            color: activeTab==='qasm' ? 'white' : '#8d8d8d',
            border: `1px solid ${activeTab==='qasm' ? '#0f62fe' : '#2a2a40'}`,
            borderRadius: 6,
            fontSize: 12,
            fontWeight: activeTab==='qasm' ? 600 : 400,
            cursor: 'pointer'
          }}
        >
          QASM 3.0 {activeTab==='qasm' ? '●' : ''}
        </button>
        <button
          onClick={()=>setActiveTab('qiskit')}
          style={{
            padding: '6px 14px',
            background: activeTab==='qiskit' ? '#0f62fe' : '#1a1a2e',
            color: activeTab==='qiskit' ? 'white' : '#8d8d8d',
            border: `1px solid ${activeTab==='qiskit' ? '#0f62fe' : '#2a2a40'}`,
            borderRadius: 6,
            fontSize: 12,
            fontWeight: activeTab==='qiskit' ? 600 : 400,
            cursor: 'pointer'
          }}
        >
          Qiskit Python {activeTab==='qiskit' ? '●' : ''}
        </button>
        <div style={{ marginLeft: 'auto', display: 'flex', gap: 6 }}>
          <button onClick={()=>activeTab==='qasm' ? setQasm(examples.Bell_QASM) : setQiskitCode(examples.Bell_Qiskit)} style={{ fontSize: 10, padding: '3px 8px', borderRadius: 12, background: '#12141f', color: '#8d8d8d', border: '1px solid #1e2235', cursor: 'pointer' }}>Bell</button>
          <button onClick={()=>activeTab==='qasm' ? setQasm(examples.VQE_H2_QASM) : setQiskitCode(examples.VQE_H2_Qiskit)} style={{ fontSize: 10, padding: '3px 8px', borderRadius: 12, background: '#12141f', color: '#8d8d8d', border: '1px solid #1e2235', cursor: 'pointer' }}>VQE H2</button>
          <button onClick={()=>activeTab==='qasm' ? setQasm(examples.QAOA_QASM) : setQiskitCode(examples.QAOA_Qiskit)} style={{ fontSize: 10, padding: '3px 8px', borderRadius: 12, background: '#12141f', color: '#8d8d8d', border: '1px solid #1e2235', cursor: 'pointer' }}>QAOA</button>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: 16 }}>
        <div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginBottom: 6, textTransform: 'uppercase', display: 'flex', justifyContent: 'space-between' }}>
            <span>{activeTab === 'qasm' ? 'QASM 3.0 Editor' : 'Qiskit Python Editor'}</span>
            <span style={{ fontSize: 10, color: '#6f6f6f' }}>{activeTab === 'qasm' ? 'OPENQASM' : 'Python • Qiskit 1.1.0'}</span>
          </div>
          <textarea
            value={activeTab === 'qasm' ? qasm : qiskitCode}
            onChange={e=>activeTab==='qasm' ? setQasm(e.target.value) : setQiskitCode(e.target.value)}
            style={{
              width: '100%',
              height: 200,
              background: '#070a14',
              color: '#c6c6c6',
              border: '1px solid #1e2235',
              borderRadius: 6,
              padding: 12,
              fontSize: 12,
              fontFamily: 'Menlo, Monaco, Consolas, monospace',
              resize: 'vertical',
              lineHeight: 1.5
            }}
            placeholder={activeTab==='qasm' ? 'OPENQASM 3.0;\nqubit[2] q;\nh q[0];\ncx q[0],q[1];' : 'from qiskit import QuantumCircuit\nqc = QuantumCircuit(2)\nqc.h(0)\nqc.cx(0,1)'}
          />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button onClick={handleAnalyze} disabled={analyzing} style={{ padding: '8px 16px', background: '#0f62fe', color: 'white', border: 'none', borderRadius: 6, fontSize: 12, fontWeight: 500, cursor: 'pointer' }}>
              {analyzing ? '...' : (locale==='ar' ? 'تحليل الدائرة' : 'Analyze Circuit')}
            </button>
            <button onClick={()=>activeTab==='qasm' ? setQasm('') : setQiskitCode('')} style={{ padding: '8px 16px', background: '#212131', color: '#c6c6c6', border: '1px solid #2a2a40', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              {locale==='ar' ? 'مسح' : 'Clear'}
            </button>
            <div style={{ marginLeft: 'auto', fontSize: 10, color: '#6f6f6f', display: 'flex', alignItems: 'center' }}>
              {activeTab==='qasm' ? 'يدعم QASM 2.0/3.0' : 'يدعم Qiskit 1.1.0 • Granite-8B'}
            </div>
          </div>
        </div>

        <div style={{ background: '#0a0e1a', border: '1px solid #1e2235', borderRadius: 6, padding: 12 }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', marginBottom: 8, display: 'flex', justifyContent: 'space-between' }}>
            <span>{locale==='ar' ? 'ملف الدائرة (Q-LEAR)' : 'Circuit Profile (Q-LEAR)'}</span>
            <span style={{ fontSize: 10, color: activeTab==='qasm' ? '#0f62fe' : '#08bdba' }}>{activeTab.toUpperCase()}</span>
          </div>
          {profile ? (
            <div style={{ fontSize: 12, color: '#c6c6c6', lineHeight: 1.7 }}>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 4 }}>
                <div>Qubits (Cw): <strong>{profile.num_qubits}</strong></div>
                <div>Depth (Cd): <strong>{profile.depth}</strong></div>
                <div>1Q (Gc1q): {profile.num_1q_gates}</div>
                <div>2Q (Gc2q): {profile.num_2q_gates}</div>
              </div>
              <div style={{ marginTop: 6 }}>Entanglement: {(profile.entanglement_ratio*100).toFixed(1)}% • Dpe: {profile.Dpe.toFixed(2)}</div>
              <div>Algorithm: <span style={{ color: '#0f62fe', fontWeight: 600 }}>{profile.algorithm_type}</span> • Lang: {profile.language}</div>
              <div style={{ marginTop: 10, padding: 8, background: 'rgba(15,98,254,0.08)', borderRadius: 4, border: '1px solid rgba(15,98,254,0.15)' }}>
                <div style={{ fontSize: 11, color: '#8d8d8d' }}>Fidelity Proxy</div>
                <div style={{ fontSize: 16, fontWeight: 300, color: '#0f62fe' }}>{(profile.estimated_fidelity_proxy*100).toFixed(1)}%</div>
                <div style={{ fontSize: 10, color: '#6f6f6f', marginTop: 4 }}>Q-LEAR: [{profile.Cw}, {profile.Cd}, {profile.Gc1q}, {profile.Gc2q}, {profile.Dpe.toFixed(1)}]</div>
              </div>
              <div style={{ marginTop: 8, fontSize: 11, color: '#24a148', background: 'rgba(36,161,72,0.08)', padding: '4px 8px', borderRadius: 4, textAlign: 'center' }}>
                {locale==='ar' ? '✓ جاهز للتنفيذ عبر Copilot' : '✓ Ready for execution via Copilot'}
              </div>
            </div>
          ) : (
            <div style={{ fontSize: 12, color: '#6f6f6f', textAlign: 'center', padding: 30 }}>
              <div style={{ fontSize: 20, marginBottom: 8 }}>⚛️</div>
              {locale==='ar' ? 'اختر تبويب QASM أو Qiskit Python وأدخل دائرتك ثم اضغط تحليل' : 'Choose QASM or Qiskit Python tab, enter circuit, then click Analyze'}
              <div style={{ fontSize: 10, marginTop: 8, color: '#4a4a5a' }}>Bell, VQE H2, QAOA examples available</div>
            </div>
          )}
        </div>
      </div>

      <div style={{ marginTop: 12, padding: 10, background: 'rgba(15,98,254,0.04)', border: '1px solid rgba(15,98,254,0.08)', borderRadius: 6 }}>
        <div style={{ fontSize: 11, color: '#0f62fe', fontWeight: 600, marginBottom: 4 }}>
          {locale==='ar' ? 'كيف تتربط بمنصات التشغيل؟' : 'How it connects to quantum execution platforms?'}
        </div>
        <div style={{ fontSize: 10, color: '#8d8d8d', lineHeight: 1.6 }}>
          {locale==='ar' ? 
          'الدائرة (QASM أو Qiskit Python) → Analyzer Q-LEAR (Cw,Cd,Gc1q,Gc2q,Dpe) → Backend Repo يجلب T1/T2/RO/CZ حية من IBM Quantum (fez 135.6us) + Drift 8M + kp 2.0 → NeuralUCB يبني 22-D Context → يختار 1 من 72 خيار → Mitigation Factory S-ZNE 1.2x → Qiskit Runtime (IBM) أو Braket (IonQ) أو Azure → Monitor + Reward → Learning Engine' :
          'Circuit (QASM or Qiskit Python) → Analyzer Q-LEAR → Backend Repo live T1/T2/RO/CZ from IBM Quantum (fez 135.6us) + Drift 8M + kp 2.0 → NeuralUCB 22-D Context → 1 of 72 arms → Mitigation S-ZNE 1.2x → Qiskit Runtime (IBM) or Braket (IonQ) or Azure → Monitor + Reward → Learning'
          }
        </div>
      </div>
    </div>
  )
}
