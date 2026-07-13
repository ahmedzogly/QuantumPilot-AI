import dynamic from 'next/dynamic'
import { LanguageProvider } from '../context/LanguageContext'
import Header from '../components/Header'

const SpaceWeatherChart = dynamic(() => import('../components/SpaceWeatherChart'), { ssr: false })
const BackendChart = dynamic(() => import('../components/BackendChart'), { ssr: false })
const TrainingChart = dynamic(() => import('../components/TrainingChart'), { ssr: false })
const DriftChart = dynamic(() => import('../components/DriftChart'), { ssr: false })
const T1vsKpChart = dynamic(() => import('../components/T1vsKpChart'), { ssr: false })
const MitigationChart = dynamic(() => import('../components/MitigationChart'), { ssr: false })
const CopilotChat = dynamic(() => import('../components/CopilotChat'), { ssr: false })

function DashboardContent() {
  return (
    <div style={{
      minHeight: '100vh',
      backgroundColor: '#0a0e1a',
      position: 'relative'
    }}>
      <Header />
      
      <main style={{ padding: '24px 32px', maxWidth: 1400, margin: '0 auto' }}>
        {/* Hero - Clean solid background, NO image behind logo - as requested */}
        <div style={{
          background: '#12141f',
          border: '1px solid #1e2235',
          borderRadius: 12,
          padding: '48px 32px',
          marginBottom: 24,
          textAlign: 'center'
        }}>
          <img src="/logo.png" alt="QuantumPilot AI Logo" style={{ width: 72, height: 72, marginBottom: 20, display: 'block', marginLeft: 'auto', marginRight: 'auto' }} />
          <h2 style={{ fontSize: 28, fontWeight: 600, color: 'white', margin: '0 0 8px 0', letterSpacing: '-0.02em' }}>QuantumPilot AI Platform</h2>
          <p style={{ fontSize: 14, color: '#8d8d8d', margin: 0 }}>Live IBM Quantum • 8.04M Records • NeuralUCB 8847 Contexts • Space Weather Aware</p>
        </div>

        <div style={{ marginBottom: 24 }}>
          <CopilotChat />
        </div>

        <div style={{ marginBottom: 24 }}>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20
          }}>
            <SpaceWeatherChart />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20
          }}>
            <BackendChart />
          </div>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20
          }}>
            <TrainingChart />
          </div>
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20
          }}>
            <DriftChart />
          </div>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20
          }}>
            <T1vsKpChart />
          </div>
        </div>

        <div style={{
          background: '#12141f',
          border: '1px solid #1e2235',
          borderRadius: 8,
          padding: 20,
          marginBottom: 24
        }}>
          <MitigationChart />
        </div>

        <div style={{
          borderTop: '1px solid #1e2235',
          paddingTop: 16,
          marginTop: 32,
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: 11,
          color: '#6f6f6f'
        }}>
          <div>QuantumPilot AI • IBM Quantum Live • Professional • No Background Image Behind Logo</div>
          <div>github.com/ahmedzogly/QuantumPilot-AI</div>
        </div>
      </main>
    </div>
  )
}

export default function Dashboard() {
  return (
    <LanguageProvider>
      <DashboardContent />
    </LanguageProvider>
  )
}
