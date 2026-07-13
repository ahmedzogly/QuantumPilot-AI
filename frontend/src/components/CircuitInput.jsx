import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function CircuitInput({ onAnalyze }) {
  const { t, locale } = useLanguage()
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
  const [algoType, setAlgoType] = useState('VQE')
  const [analyzing, setAnalyzing] = useState(false)
  const [profile, setProfile] = useState(null)

  const examples = {
    Bell: `OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
h q[0];
cx q[0], q[1];
c = measure q;`,
    VQE_H2: `OPENQASM 3.0;
include "stdgates.inc";
qubit[2] q;
bit[2] c;
ry(1.0) q[0];
ry(1.0) q[1];
cx q[0], q[1];
ry(0.5) q[0];
c = measure q;`,
    QAOA: `OPENQASM 3.0;
include "stdgates.inc";
qubit[3] q;
bit[3] c;
h q[0]; h q[1]; h q[2];
rzz(0.5) q[0], q[1];
rzz(0.5) q[1], q[2];
rx(0.3) q;
c = measure q;`
  }

  const handleAnalyze = async () => {
    setAnalyzing(true)
    // Simulate analyzer - in production call POST /api/v1/analyze
    try {
      // Mock profile based on QASM content
      const lines = qasm.split('\n').length
      const hasCX = (qasm.match(/cx/g) || []).length
      const hasH = (qasm.match(/h /g) || []).length
      const numQubits = qasm.match(/qubit\[(\d+)\]/) ? parseInt(qasm.match(/qubit\[(\d+)\]/)[1]) : 3
      
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
        estimated_fidelity_proxy: 0.85 + (numQubits * 0.02)
      }
      setProfile(mockProfile)
      if (onAnalyze) onAnalyze(mockProfile, qasm)
    } catch (e) {
      console.error(e)
    }
    setAnalyzing(false)
  }

  const handleFileUpload = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onload = (ev) => setQasm(ev.target.result)
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
            {locale === 'ar' ? 'أين يدخل الباحث دائرته - QASM 3.0، Qiskit، أو توليد بالذكاء الاصطناعي' : 'Where researcher enters circuit - QASM 3.0, Qiskit, or AI generation'}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          <select value={algoType} onChange={e=>setAlgoType(e.target.value)} style={{ padding: '6px 10px', background: '#0f111a', color: '#c6c6c6', border: '1px solid #1e2235', borderRadius: 6, fontSize: 12 }}>
            <option value="VQE">VQE</option>
            <option value="QAOA">QAOA</option>
            <option value="Grover">Grover</option>
            <option value="QFT">QFT</option>
            <option value="Custom">Custom</option>
          </select>
        </div>
      </div>

      <div style={{ display: 'flex', gap: 6, marginBottom: 12, flexWrap: 'wrap' }}>
        <span style={{ fontSize: 11, color: '#8d8d8d' }}>{locale==='ar' ? 'أمثلة:' : 'Examples:'}</span>
        {Object.keys(examples).map(key => (
          <button key={key} onClick={()=>setQasm(examples[key])} style={{ fontSize: 11, padding: '3px 8px', borderRadius: 12, background: '#1a1a2e', color: '#c6c6c6', border: '1px solid #2a2a40', cursor: 'pointer' }}>{key}</button>
        ))}
        <label style={{ fontSize: 11, padding: '3px 8px', borderRadius: 12, background: '#0f62fe', color: 'white', border: '1px solid #0f62fe', cursor: 'pointer' }}>
          {locale==='ar' ? 'رفع ملف' : 'Upload File'}
          <input type="file" accept=".qasm,.qpy,.py,.txt" onChange={handleFileUpload} style={{ display: 'none' }} />
        </label>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 0.8fr', gap: 16 }}>
        <div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginBottom: 6, textTransform: 'uppercase' }}>QASM 3.0 / Qiskit Code</div>
          <textarea
            value={qasm}
            onChange={e=>setQasm(e.target.value)}
            style={{
              width: '100%',
              height: 180,
              background: '#0a0e1a',
              color: '#c6c6c6',
              border: '1px solid #1e2235',
              borderRadius: 6,
              padding: 12,
              fontSize: 12,
              fontFamily: 'Menlo, Monaco, monospace',
              resize: 'vertical'
            }}
            placeholder={locale==='ar' ? 'الصق كود QASM هنا...' : 'Paste QASM code here...'}
          />
          <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
            <button onClick={handleAnalyze} disabled={analyzing} style={{ padding: '8px 16px', background: '#0f62fe', color: 'white', border: 'none', borderRadius: 6, fontSize: 12, fontWeight: 500, cursor: 'pointer' }}>
              {analyzing ? '...' : (locale==='ar' ? 'تحليل الدائرة' : 'Analyze Circuit')}
            </button>
            <button onClick={()=>setQasm('')} style={{ padding: '8px 16px', background: '#212131', color: '#c6c6c6', border: '1px solid #2a2a40', borderRadius: 6, fontSize: 12, cursor: 'pointer' }}>
              {locale==='ar' ? 'مسح' : 'Clear'}
            </button>
          </div>
          <div style={{ fontSize: 11, color: '#6f6f6f', marginTop: 8 }}>
            {locale==='ar' ? 'يدعم: QASM 2.0/3.0، Qiskit Python، أو توليد عبر Granite-8B' : 'Supports: QASM 2.0/3.0, Qiskit Python, or Granite-8B generation'}
          </div>
        </div>

        <div style={{ background: '#0a0e1a', border: '1px solid #1e2235', borderRadius: 6, padding: 12 }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', marginBottom: 8 }}>
            {locale==='ar' ? 'ملف الدائرة (Q-LEAR Features)' : 'Circuit Profile (Q-LEAR)'}
          </div>
          {profile ? (
            <div style={{ fontSize: 12, color: '#c6c6c6', lineHeight: 1.6 }}>
              <div>Qubits (Cw): {profile.num_qubits} • Depth (Cd): {profile.depth}</div>
              <div>1Q Gates (Gc1q): {profile.num_1q_gates} • 2Q Gates (Gc2q): {profile.num_2q_gates}</div>
              <div>Entanglement: {(profile.entanglement_ratio*100).toFixed(1)}% • Dpe: {profile.Dpe.toFixed(2)}</div>
              <div>Algorithm: {profile.algorithm_type} • Width: {profile.width}</div>
              <div style={{ marginTop: 8, padding: 8, background: 'rgba(15,98,254,0.1)', borderRadius: 4, border: '1px solid rgba(15,98,254,0.2)' }}>
                Fidelity Proxy: {(profile.estimated_fidelity_proxy*100).toFixed(1)}%<br/>
                Q-LEAR Vector: [{profile.Cw}, {profile.Cd}, {profile.Gc1q}, {profile.Gc2q}, {profile.Dpe.toFixed(1)}]
              </div>
              <div style={{ marginTop: 8, fontSize: 11, color: '#24a148' }}>
                {locale==='ar' ? '✓ جاهز للتنفيذ عبر Copilot' : '✓ Ready for execution via Copilot'}
              </div>
            </div>
          ) : (
            <div style={{ fontSize: 12, color: '#6f6f6f', textAlign: 'center', padding: 20 }}>
              {locale==='ar' ? 'اضغط تحليل الدائرة لرؤية ملف Q-LEAR' : 'Click Analyze to see Q-LEAR profile'}
            </div>
          )}
        </div>
      </div>

      <div style={{ marginTop: 16, padding: 12, background: 'rgba(15,98,254,0.05)', border: '1px solid rgba(15,98,254,0.1)', borderRadius: 6 }}>
        <div style={{ fontSize: 11, color: '#0f62fe', fontWeight: 600, marginBottom: 4 }}>
          {locale==='ar' ? 'كيف تتربط بمنصات التشغيل؟' : 'How it connects to quantum execution platforms?'}
        </div>
        <div style={{ fontSize: 11, color: '#8d8d8d', lineHeight: 1.5 }}>
          {locale==='ar' ? 
          'الدائرة تدخل هنا → Analyzer يحسب Q-LEAR (Cw,Cd,Gc1q,Gc2q,Dpe) → Backend Repo يجلب T1/T2/RO/CZ حية من IBM Quantum (fez 135.6us) + Drift 8M + kp 2.0 → NeuralUCB يبني 22-D Context (Backend 8 + Circuit 7 + History 3 + Env 2 kp,temp) → يختار 1 من 72 خيار (3 backends ×4 opt×6 mitigation) → Mitigation Factory S-ZNE 1.2x → Qiskit Runtime (IBM) أو Braket (IonQ) أو Azure → Monitor QCalEval + SpaceWeather → Reward → Learning Engine يحدث A_grad' :
          'Circuit entered here → Analyzer computes Q-LEAR (Cw,Cd,Gc1q,Gc2q,Dpe) → Backend Repo fetches live T1/T2/RO/CZ from IBM Quantum (fez 135.6us) + Drift 8M + kp 2.0 → NeuralUCB builds 22-D Context (Backend 8 + Circuit 7 + History 3 + Env 2) → Selects 1 of 72 arms (3 backends×4 opt×6 mit) → Mitigation Factory S-ZNE 1.2x → Qiskit Runtime (IBM) or Braket (IonQ) or Azure → Monitor QCalEval + SpaceWeather → Reward → Learning Engine updates A_grad'
          }
        </div>
      </div>
    </div>
  )
}
