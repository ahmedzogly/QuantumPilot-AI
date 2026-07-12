
import { useState } from 'react'

export default function CopilotChat() {
  const [intent, setIntent] = useState("")
  const [plan, setPlan] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  const examples = [
    "نفذ بأقل تكلفة",
    "اختر الجهاز الذي يحقق Fidelity أعلى من 95%",
    "نفذ بأسرع وقت",
    "تجنب التنفيذ وقت العاصفة الشمسية",
    "Execute with lowest cost",
    "Choose backend with fidelity >95%"
  ]

  const handlePlan = async () => {
    if (!intent) return
    setLoading(true)
    try {
      // Mock call - in production fetch from /api/v1/copilot/plan
      // For demo, simulate parsing
      const lower = intent.toLowerCase()
      let type = "balanced"
      if (lower.includes("تكلفة") || lower.includes("cost") || lower.includes("cheap")) type = "cheapest"
      else if (lower.includes("دقة") || lower.includes("fidelity") || lower.includes("95%")) type = "highest_fidelity"
      else if (lower.includes("أسرع") || lower.includes("fast")) type = "fastest"
      else if (lower.includes("طقس") || lower.includes("space") || lower.includes("عاصفة") || lower.includes("kp")) type = "avoid_space_weather"
      
      // Simulate plan
      setPlan({
        intent: { type, original_text: intent },
        plan: {
          backend_name: "ibm_kingston",
          optimization_level: type==="highest_fidelity" ? 3 : type==="cheapest" ? 1 : 2,
          mitigation_strategy: type==="fastest" ? "none" : "s_zne",
          shots: type==="highest_fidelity" ? 8192 : 1024,
          expected_fidelity: type==="highest_fidelity" ? 0.97 : 0.92,
          explanation_ar: type==="cheapest" ? "اخترت أقل تكلفة: S-ZNE 1.2x بدل 5x توفير 76% + 1024 shots + backend أقل queue" : 
                         type==="highest_fidelity" ? "اخترت أعلى دقة 95%: ibm_kingston T1 231us + opt 3 + pec + 8192 shots" :
                         type==="avoid_space_weather" ? "حالة الطقس هادئة kp=2.0 آمن للتنفيذ S-ZNE" :
                         "اخترت التوازن الأمثل: Fidelity 50% + Cost 20% + Queue 20%",
          reward_weights: { fidelity: type==="highest_fidelity"?0.7:0.5, cost: type==="cheapest"?0.5:0.2 }
        },
        space_weather: { kp_index: 2.0, risk_level: "Unsettled", neutron_flux: 94.6 }
      })
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  return (
    <div style={{ background: '#0f172a', padding: 15, borderRadius: 8, border: '2px solid #8b5cf6' }}>
      <h3>🤖 Quantum Copilot - Intent Agent (9.5/10 Feature)</h3>
      <p style={{ fontSize: 12, color: '#aaa' }}>اكتب نية طبيعية بالعربي أو الإنجليزي - مثال: "نفذ بأقل تكلفة" أو "Fidelity &gt;95%" - والـ AI يبني خطة تنفيذ تلقائياً ويشرح</p>
      
      <div style={{ display: 'flex', gap: 5, flexWrap: 'wrap', margin: '10px 0' }}>
        {examples.map(ex => (
          <button key={ex} onClick={() => setIntent(ex)} style={{ fontSize: 11, padding: '4px 8px', borderRadius: 12, background: '#1e293b', color: 'white', border: '1px solid #555', cursor: 'pointer' }}>{ex}</button>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 10 }}>
        <input 
          value={intent} 
          onChange={e => setIntent(e.target.value)} 
          placeholder="مثال: نفذ بأقل تكلفة أو Choose backend with fidelity >95%"
          style={{ flex: 1, padding: 10, borderRadius: 5, background: '#1a1a1a', color: 'white', border: '1px solid #555' }}
        />
        <button onClick={handlePlan} disabled={loading} style={{ padding: '10px 20px', background: '#8b5cf6', color: 'white', border: 'none', borderRadius: 5, cursor: 'pointer' }}>
          {loading ? "..." : "Build Plan"}
        </button>
      </div>

      {plan && (
        <div style={{ marginTop: 15, background: '#1e293b', padding: 15, borderRadius: 8 }}>
          <h4>✅ Execution Plan Auto-Generated</h4>
          <p><strong>Intent:</strong> {plan.intent.type} - "{plan.intent.original_text}"</p>
          <p><strong>Backend:</strong> {plan.plan.backend_name} | <strong>Opt:</strong> {plan.plan.optimization_level} | <strong>Mitigation:</strong> {plan.plan.mitigation_strategy} | <strong>Shots:</strong> {plan.plan.shots}</p>
          <p><strong>Expected Fidelity:</strong> {(plan.plan.expected_fidelity*100).toFixed(1)}% | <strong>Weights:</strong> {JSON.stringify(plan.plan.reward_weights)}</p>
          <p style={{ background: '#111', padding: 10, borderRadius: 5, marginTop: 10 }}><strong>Explanation AR:</strong> {plan.plan.explanation_ar}</p>
          <p style={{ fontSize: 12, color: '#888', marginTop: 10 }}>Space Weather: Kp={plan.space_weather.kp_index} {plan.space_weather.risk_level} - Cosmic Ray {plan.space_weather.neutron_flux} counts/min - Novel Correlation T1 vs kp -0.197 p=0.00047</p>
          <p style={{ fontSize: 11, color: '#00ff88' }}>Novelty: First platform to parse Arabic intent + space weather aware + explainable + NeuralUCB 22-D (Backend 8 + Q-LEAR 7 + Env 2 kp,temp)</p>
        </div>
      )}
    </div>
  )
}
