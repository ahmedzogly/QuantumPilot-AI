import { useState, useEffect } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function UncertaintyChart() {
  const { t, locale } = useLanguage()
  const [explanation, setExplanation] = useState(null)

  useEffect(() => {
    // Mock explainability data from DriftTransformerExplainable
    // In production, fetch from /api/v1/explain/drift
    setExplanation({
      predicted_T1: 45.2,
      uncertainty_std: 8.3,
      confidence: "84.2%",
      temporal_importance: {
        "t-9": 0.05, "t-8": 0.13, "t-7": 0.08, "t-6": 0.06, "t-5": 0.07,
        "t-4": 0.11, "t-3": 0.18, "t-2": 0.22, "t-1": 0.07, "t-0": 0.03
      },
      most_important_time: "t-2 (importance 0.22) - Kp spike 2 steps ago",
      feature_importance: {
        "T1": 0.12, "T2": 0.10, "Kp": 0.28, "Neutron": 0.15, "Temp": 0.08, "Solar": 0.09, "RO": 0.10, "CZ": 0.08
      },
      most_important_feature: "Kp (importance 0.28) - Geomagnetic storm",
      interpretation: locale === 'ar' 
        ? "النموذج يتوقع T1 المستقبلي = 45.2us مع عدم يقين ±8.3us (ثقة 84.2%). أهم ميزة: Kp (0.28) - عاصفة مغناطيسية. أهم نقطة زمنية: t-2 (0.22) - ارتفاع Kp قبل خطوتين يؤثر بقوة على انخفاض T1 المستقبلي - يشير لعاصفة شمسية قادمة ستؤثر على الكيوبت."
        : "Model predicts future T1 = 45.2us with uncertainty ±8.3us (confidence 84.2%). Most important feature: Kp (0.28) - Geomagnetic storm. Most attended time: t-2 (0.22) - Kp spike 2 steps ago strongly influences future T1 drop - indicating incoming solar storm will affect qubit."
    })
  }, [locale])

  if (!explanation) return <div>Loading explainability...</div>

  const temporalData = Object.entries(explanation.temporal_importance).map(([time, imp]) => ({ time, importance: imp }))
  const featureData = Object.entries(explanation.feature_importance).map(([feat, imp]) => ({ feature: feat, importance: imp }))

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>
          {locale==='ar' ? 'تقدير عدم اليقين والشرح - Attention Weights' : 'Uncertainty Estimation & Explainability - Attention Weights'}
        </h3>
        <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>
          {locale==='ar' ? 'يوضح أي نقطة زمنية وأي ميزة بيئية أثرت أكثر في التنبؤ' : 'Shows which time points and which environmental features affected prediction most'}
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 12, marginBottom: 16 }}>
        <div style={{ background: '#0f111a', border: '1px solid #1e2235', borderRadius: 8, padding: 12, textAlign: 'center' }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase' }}>{locale==='ar' ? 'التنبؤ' : 'Prediction'}</div>
          <div style={{ fontSize: 22, fontWeight: 300, color: '#f4f4f4', marginTop: 4 }}>{explanation.predicted_T1}µs</div>
          <div style={{ fontSize: 11, color: '#8d8d8d' }}>T1 Future</div>
        </div>
        <div style={{ background: '#0f111a', border: '1px solid #1e2235', borderRadius: 8, padding: 12, textAlign: 'center' }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase' }}>{locale==='ar' ? 'عدم اليقين' : 'Uncertainty'}</div>
          <div style={{ fontSize: 20, fontWeight: 300, color: '#f1c21b', marginTop: 4 }}>±{explanation.uncertainty_std}µs</div>
          <div style={{ fontSize: 11, color: '#8d8d8d' }}>{explanation.confidence} confidence</div>
        </div>
        <div style={{ background: 'rgba(15,98,254,0.08)', border: '1px solid rgba(15,98,254,0.2)', borderRadius: 8, padding: 12, textAlign: 'center' }}>
          <div style={{ fontSize: 11, color: '#0f62fe', textTransform: 'uppercase' }}>{locale==='ar' ? 'أهم ميزة' : 'Top Feature'}</div>
          <div style={{ fontSize: 14, fontWeight: 600, color: '#0f62fe', marginTop: 4 }}>{explanation.most_important_feature}</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>{explanation.most_important_time}</div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16, marginBottom: 16 }}>
        <div>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', marginBottom: 8 }}>{locale==='ar' ? 'أهمية النقاط الزمنية - أي وقت في الماضي أثر أكثر؟' : 'Temporal Importance - Which past time points mattered most?'}</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {temporalData.sort((a,b)=>b.importance-a.importance).slice(0,5).map((d,i) => (
              <div key={d.time} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ fontSize: 11, color: '#8d8d8d', width: 40 }}>{d.time}</div>
                <div style={{ flex: 1, height: 6, background: '#0f111a', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${d.importance*400}%`, background: i===0 ? '#0f62fe' : '#2a2a40', borderRadius: 3 }} />
                </div>
                <div style={{ fontSize: 11, color: '#c6c6c6', width: 40, textAlign: 'right' }}>{(d.importance*100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 10, color: '#6f6f6f', marginTop: 8 }}>
            {locale==='ar' ? 'مثال: t-2 أهم نقطة يعني ارتفاع Kp قبل خطوتين يؤثر بقوة على انخفاض T1 المستقبلي' : 'Example: t-2 most important means Kp spike 2 steps ago strongly influences future T1 drop'}
          </div>
        </div>

        <div>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', marginBottom: 8 }}>{locale==='ar' ? 'أهمية الميزات البيئية - أي ميزة أثرت أكثر؟' : 'Environmental Feature Importance - Which feature mattered most?'}</div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
            {featureData.sort((a,b)=>b.importance-a.importance).map((d,i) => (
              <div key={d.feature} style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <div style={{ fontSize: 11, color: '#8d8d8d', width: 60 }}>{d.feature}</div>
                <div style={{ flex: 1, height: 6, background: '#0f111a', borderRadius: 3, overflow: 'hidden' }}>
                  <div style={{ height: '100%', width: `${d.importance*400}%`, background: d.feature==='Kp' ? '#da1e28' : d.feature==='Neutron' ? '#ff832b' : i===0 ? '#0f62fe' : '#2a2a40', borderRadius: 3 }} />
                </div>
                <div style={{ fontSize: 11, color: '#c6c6c6', width: 40, textAlign: 'right' }}>{(d.importance*100).toFixed(1)}%</div>
              </div>
            ))}
          </div>
          <div style={{ fontSize: 10, color: '#6f6f6f', marginTop: 8 }}>
            {locale==='ar' ? 'Kp أحمر يعني عاصفة مغناطيسية - Neutron برتقالي يعني أشعة كونية' : 'Kp red = geomagnetic storm - Neutron orange = cosmic ray'}
          </div>
        </div>
      </div>

      <div style={{ background: '#0a0e1a', border: '1px solid #1e2235', borderRadius: 6, padding: 12 }}>
        <div style={{ fontSize: 11, color: '#0f62fe', fontWeight: 600, marginBottom: 4 }}>
          {locale==='ar' ? 'التفسير البشري' : 'Human-readable Interpretation'}
        </div>
        <div style={{ fontSize: 12, color: '#c6c6c6', lineHeight: 1.6 }}>
          {explanation.interpretation}
        </div>
        <div style={{ fontSize: 10, color: '#6f6f6f', marginTop: 8 }}>
          Attention Weights shape: [batch=1, nhead=4, seq=10, seq=10] - Each head attends to different time patterns, averaged over 2 layers. For last prediction (t=0), attention from t=0 to all past t-9..t-0 shows which past moments influenced future. Combined with gradient-based feature importance (T1,T2,Kp,Neutron,Temp,Solar,RO,CZ) gives full explainability.
        </div>
      </div>
    </div>
  )
}
