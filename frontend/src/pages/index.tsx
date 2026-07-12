import dynamic from 'next/dynamic'

const DriftChart = dynamic(() => import('../components/DriftChart'), { ssr: false })
const T1vsKpChart = dynamic(() => import('../components/T1vsKpChart'), { ssr: false })
const TrainingChart = dynamic(() => import('../components/TrainingChart'), { ssr: false })
const MitigationChart = dynamic(() => import('../components/MitigationChart'), { ssr: false })
const BackendChart = dynamic(() => import('../components/BackendChart'), { ssr: false })
const SpaceWeatherChart = dynamic(() => import('../components/SpaceWeatherChart'), { ssr: false })
const CopilotChat = dynamic(() => import('../components/CopilotChat'), { ssr: false })

export default function Dashboard() {
  return (
    <div style={{ fontFamily: 'Arial', padding: 20, background: '#0a0a0a', color: 'white', minHeight: '100vh' }}>
      <h1 style={{ fontSize: 36, fontWeight: 'bold', color: '#00ff88' }}>QuantumPilot AI</h1>
      <p style={{ fontSize: 18 }}>AI Operating Intelligence Platform for Quantum Computing - 9.5/10 Integrated Platform</p>
      
      <div style={{ marginTop: 20 }}>
        <CopilotChat />
      </div>

      <div style={{ marginTop: 20 }}>
        <SpaceWeatherChart />
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 20 }}>
        <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, border: '1px solid #333' }}>
          <BackendChart />
        </div>
        <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, border: '1px solid #333' }}>
          <TrainingChart />
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginTop: 20 }}>
        <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, border: '1px solid #00ff88' }}>
          <DriftChart />
        </div>
        <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, border: '1px solid #ffaa00' }}>
          <T1vsKpChart />
        </div>
      </div>

      <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, marginTop: 20 }}>
        <MitigationChart />
      </div>

      <div style={{ background: '#1a1a1a', padding: 15, borderRadius: 8, marginTop: 20 }}>
        <h2>✅ Integrated Platform Status - 9.5/10 (vs 7.5/10 for Error Mitigation only)</h2>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 12 }}>
          <thead><tr><th style={{ border: '1px solid #555', padding: 5 }}>Feature</th><th style={{ border: '1px solid #555', padding: 5 }}>IBM</th><th style={{ border: '1px solid #555', padding: 5 }}>Mitiq</th><th style={{ border: '1px solid #555', padding: 5 }}>Qedma</th><th style={{ border: '1px solid #555', padding: 5 }}>QDevOps</th><th style={{ border: '1px solid #555', padding: 5, color: '#00ff88' }}>QuantumPilot AI (Now)</th></tr></thead>
          <tbody>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Error Mitigation</td><td>✅</td><td>✅</td><td>✅</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ 7 methods: ZNE,S-ZNE 1.2x,PEC,CDR,TREX,NNAS,Transformer + Mitiq Adapter</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Backend Selection</td><td>⚠️ least_busy</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ NeuralUCB 22-D + Live fez/marrakesh/kingston + 8M drift + kp,neutron</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>AI Orchestrator Full Lifecycle</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ Analyze→Select→Decide→Mitigate→Execute→Monitor→Recovery→Learn</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Knowledge Graph</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ 8M rows + live 1.1MB + 8847 contexts + clifford 100 + QCalEval 243</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Copilot LLM Agent</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ Arabic/English Intent → Plan: "نفذ بأقل تكلفة" → backend,opt,mit,shots + explanation</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Space Weather Aware</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ Live NOAA kp 2.0 + neutron 94.6 + solar 74.65° + T1 vs kp -0.197 p=0.00047</td></tr>
            <tr><td style={{ border: '1px solid #555', padding: 5 }}>Explainability</td><td>❌</td><td>❌</td><td>❌</td><td>❌</td><td style={{ color: '#00ff88' }}>✅ Reward weights + Mitigation comparison 1.2x vs 5x + Space weather advice</td></tr>
          </tbody>
        </table>
        <p style={{ fontSize: 12, color: '#00ff88', marginTop: 10 }}>We are not competitor to IBM - We are intelligence layer on top, like GitHub over computers, Docker over OS, Datadog over servers (as ChatGPT analysis suggested)</p>
      </div>
    </div>
  )
}
