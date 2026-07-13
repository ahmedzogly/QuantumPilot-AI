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
const CircuitInput = dynamic(() => import('../components/CircuitInput'), { ssr: false })

function DashboardContent() {
  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#070a14', position: 'relative' }}>
      <div style={{
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        backgroundImage: 'url(/background.png)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        opacity: 0.80,
        zIndex: 0
      }} />
      <div style={{
        position: 'fixed',
        top: 0, left: 0, right: 0, bottom: 0,
        background: 'linear-gradient(180deg, rgba(7,10,20,0.20) 0%, rgba(7,10,20,0.45) 100%)',
        zIndex: 1
      }} />

      <div style={{ position: 'relative', zIndex: 2 }}>
        <Header />
        
        <main style={{ padding: '24px 32px', maxWidth: 1400, margin: '0 auto' }}>
          <div style={{
            background: '#12141f',
            border: '1px solid #1e2235',
            borderRadius: 12,
            padding: '48px 32px',
            marginBottom: 24,
            textAlign: 'center'
          }}>
            <img src="/logo.png" alt="QuantumPilot AI Logo" style={{ width: 72, height: 72, marginBottom: 20, display: 'block', marginLeft: 'auto', marginRight: 'auto', borderRadius: '20px' }} />
            <h2 style={{ fontSize: 28, fontWeight: 600, color: 'white', margin: '0 0 8px 0' }}>QuantumPilot AI Platform</h2>
            <p style={{ fontSize: 14, color: '#8d8d8d', margin: 0 }}>Live IBM Quantum • 8.04M Records • NeuralUCB 8847 Contexts • Space Weather Aware • Cards 30% Transparency</p>
          </div>

          <div style={{
            background: 'rgba(18, 20, 31, 0.70)',
            backdropFilter: 'blur(20px)',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20,
            marginBottom: 24
          }}>
            <CircuitInput />
          </div>

          <div style={{ marginBottom: 24 }}>
            <div style={{
              background: 'rgba(18, 20, 31, 0.70)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <CopilotChat />
            </div>
          </div>

          <div style={{ marginBottom: 24 }}>
            <div style={{
              background: 'rgba(18, 20, 31, 0.70)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <SpaceWeatherChart />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
            <div style={{ background: 'rgba(18, 20, 31, 0.70)', backdropFilter: 'blur(20px)', border: '1px solid #1e2235', borderRadius: 8, padding: 20 }}>
              <BackendChart />
            </div>
            <div style={{ background: 'rgba(18, 20, 31, 0.70)', backdropFilter: 'blur(20px)', border: '1px solid #1e2235', borderRadius: 8, padding: 20 }}>
              <TrainingChart />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
            <div style={{ background: 'rgba(18, 20, 31, 0.70)', backdropFilter: 'blur(20px)', border: '1px solid #1e2235', borderRadius: 8, padding: 20 }}>
              <DriftChart />
            </div>
            <div style={{ background: 'rgba(18, 20, 31, 0.70)', backdropFilter: 'blur(20px)', border: '1px solid #1e2235', borderRadius: 8, padding: 20 }}>
              <T1vsKpChart />
            </div>
          </div>

          <div style={{ background: 'rgba(18, 20, 31, 0.70)', backdropFilter: 'blur(20px)', border: '1px solid #1e2235', borderRadius: 8, padding: 20, marginBottom: 24 }}>
            <MitigationChart />
          </div>
        </main>
      </div>
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
