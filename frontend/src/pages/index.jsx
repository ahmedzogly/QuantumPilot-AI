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
      backgroundImage: 'url(/background.png)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      backgroundAttachment: 'fixed',
      position: 'relative'
    }}>
      {/* Dark overlay for readability - enterprise level */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        background: 'linear-gradient(135deg, rgba(10, 14, 26, 0.92) 0%, rgba(10, 10, 15, 0.88) 100%)',
        zIndex: 0
      }} />

      <div style={{ position: 'relative', zIndex: 1 }}>
        <Header />
        
        <main style={{ padding: '24px 32px', maxWidth: 1400, margin: '0 auto' }}>
          {/* Hero with background + logo as requested */}
          <div style={{
            background: 'rgba(18, 20, 31, 0.6)',
            backdropFilter: 'blur(20px)',
            border: '1px solid rgba(30, 34, 53, 0.5)',
            borderRadius: 12,
            padding: 32,
            marginBottom: 24,
            textAlign: 'center',
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              opacity: 0.04,
              zIndex: 0
            }}>
              <img src="/logo.png" alt="background logo" style={{ width: 400, height: 400, objectFit: 'contain' }} />
            </div>
            <div style={{ position: 'relative', zIndex: 1 }}>
              <img src="/logo.png" alt="QuantumPilot AI" style={{ width: 80, height: 80, marginBottom: 16, filter: 'drop-shadow(0 0 20px rgba(15, 98, 254, 0.4))' }} />
              <h2 style={{ fontSize: 24, fontWeight: 600, color: 'white', margin: '0 0 8px 0' }}>QuantumPilot AI Platform</h2>
              <p style={{ fontSize: 14, color: '#8d8d8d', margin: 0 }}>Live IBM Quantum • 8.04M Records • NeuralUCB 8847 Contexts • Space Weather Aware</p>
            </div>
          </div>

          <div style={{ marginBottom: 24 }}>
            <CopilotChat />
          </div>

          <div style={{ marginBottom: 24 }}>
            <div style={{
              background: 'rgba(18, 20, 31, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <SpaceWeatherChart />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
            <div style={{
              background: 'rgba(18, 20, 31, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <BackendChart />
            </div>
            <div style={{
              background: 'rgba(18, 20, 31, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <TrainingChart />
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, marginBottom: 24 }}>
            <div style={{
              background: 'rgba(18, 20, 31, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <DriftChart />
            </div>
            <div style={{
              background: 'rgba(18, 20, 31, 0.7)',
              backdropFilter: 'blur(20px)',
              border: '1px solid #1e2235',
              borderRadius: 8,
              padding: 20
            }}>
              <T1vsKpChart />
            </div>
          </div>

          <div style={{
            background: 'rgba(18, 20, 31, 0.7)',
            backdropFilter: 'blur(20px)',
            border: '1px solid #1e2235',
            borderRadius: 8,
            padding: 20,
            marginBottom: 24
          }}>
            <MitigationChart />
          </div>

          <div style={{
            borderTop: '1px solid rgba(30, 34, 53, 0.5)',
            paddingTop: 16,
            marginTop: 32,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            fontSize: 11,
            color: '#6f6f6f'
          }}>
            <div>QuantumPilot AI • IBM Quantum Live • Apache 2.0</div>
            <div>github.com/ahmedzogly/QuantumPilot-AI</div>
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
