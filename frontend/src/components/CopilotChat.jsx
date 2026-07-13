import { useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function CopilotChat() {
  const { t, locale } = useLanguage()
  const [intent, setIntent] = useState("")
  const [plan, setPlan] = useState(null)
  const [loading, setLoading] = useState(false)

  const examples = locale === 'ar' ? [
    "نفذ بأقل تكلفة",
    "اختر جهاز بدقة أعلى من 95%",
    "نفذ بأسرع وقت",
    "تجنب العاصفة الشمسية"
  ] : [
    "Execute with lowest cost",
    "Choose high fidelity backend",
    "Fastest execution",
    "Avoid space weather storm"
  ]

  const handlePlan = async () => {
    if (!intent) return
    setLoading(true)
    try {
      const lower = intent.toLowerCase()
      let type = "balanced"
      if (lower.includes("تكلفة") || lower.includes("cost") || lower.includes("cheap")) type = "cheapest"
      else if (lower.includes("دقة") || lower.includes("fidelity") || lower.includes("95")) type = "highest_fidelity"
      else if (lower.includes("أسرع") || lower.includes("fast")) type = "fastest"
      else if (lower.includes("طقس") || lower.includes("space") || lower.includes("عاصفة") || lower.includes("kp")) type = "avoid_space_weather"
      
      setPlan({
        intent: { type, original_text: intent },
        plan: {
          backend_name: "ibm_kingston",
          optimization_level: type==="highest_fidelity" ? 3 : type==="cheapest" ? 1 : 2,
          mitigation_strategy: type==="fastest" ? "none" : "s_zne",
          shots: type==="highest_fidelity" ? 8192 : 1024,
          expected_fidelity: type==="highest_fidelity" ? 0.97 : 0.92,
          explanation: type==="cheapest" ? (locale==='ar' ? "تم اختيار أقل تكلفة: S-ZNE بتكلفة 1.2x بدلاً من 5x، توفير 76%." : "Selected lowest cost: S-ZNE 1.2x vs 5x, 76% saving.") : 
                       type==="highest_fidelity" ? (locale==='ar' ? "تم اختيار أعلى دقة: ibm_kingston T1 231us، تحسين مستوى 3." : "Selected highest fidelity: ibm_kingston T1 231us, opt level 3.") :
                       (locale==='ar' ? "تم اختيار التوازن الأمثل." : "Selected balanced optimal."),
          reward_weights: { fidelity: type==="highest_fidelity"?0.7:0.5, cost: type==="cheapest"?0.5:0.2 }
        },
        space_weather: { kp_index: 2.0, risk_level: locale==='ar' ? "هادئ نسبياً" : "Unsettled", neutron_flux: 94.6 }
      })
    } catch (e) {
      console.error(e)
    }
    setLoading(false)
  }

  return (
    <div style={{
      background: '#12141f',
      border: '1px solid #1e2235',
      borderRadius: 8,
      padding: 20
    }}>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>{t('copilot_title')}</h3>
        <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>{t('copilot_subtitle')}</p>
      </div>
      
      <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 12 }}>
        {examples.map(ex => (
          <button key={ex} onClick={() => setIntent(ex)} style={{ fontSize: 11, padding: '5px 10px', borderRadius: 16, background: '#1a1a2e', color: '#c6c6c6', border: '1px solid #2a2a40', cursor: 'pointer' }}>{ex}</button>
        ))}
      </div>

      <div style={{ display: 'flex', gap: 8 }}>
        <input 
          value={intent} 
          onChange={e => setIntent(e.target.value)} 
          placeholder={t('copilot_placeholder')}
          style={{ flex: 1, padding: '10px 12px', borderRadius: 6, background: '#0f111a', color: '#f4f4f4', border: '1px solid #1e2235', fontSize: 13 }}
        />
        <button onClick={handlePlan} disabled={loading} style={{ padding: '10px 16px', background: '#0f62fe', color: 'white', border: 'none', borderRadius: 6, fontSize: 13, fontWeight: 500, cursor: 'pointer' }}>
          {loading ? "..." : t('build_plan')}
        </button>
      </div>

      {plan && (
        <div style={{ marginTop: 16, background: '#0f111a', border: '1px solid #1e2235', padding: 14, borderRadius: 6 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 8 }}>
            <span style={{ fontSize: 12, color: '#8d8d8d', textTransform: 'uppercase' }}>{t('plan')}</span>
            <span style={{ fontSize: 11, color: '#24a148', background: 'rgba(36,161,72,0.1)', padding: '2px 8px', borderRadius: 10 }}>{plan.intent.type}</span>
          </div>
          <div style={{ fontSize: 13, color: '#c6c6c6', lineHeight: 1.5 }}>
            <div>{t('backend')}: {plan.plan.backend_name} • {t('optimization')}: {plan.plan.optimization_level} • {t('mitigation_strategy')}: {plan.plan.mitigation_strategy} • {t('shots')}: {plan.plan.shots}</div>
            <div style={{ marginTop: 8, padding: 10, background: '#12141f', borderRadius: 4, fontSize: 12, color: '#8d8d8d' }}>{plan.plan.explanation}</div>
          </div>
        </div>
      )}
    </div>
  )
}
