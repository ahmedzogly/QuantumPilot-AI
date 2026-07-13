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
    <div style={{ background: '#0a0a0a', minHeight: '100vh' }}>
      <Header />
      
      <main style={{ padding: '24px 32px', maxWidth: 1400, margin: '0 auto' }}>
        {/* Copilot - Primary Action */}
        <div style={{ marginBottom: 24 }}>
          <CopilotChat />
        </div>

        {/* Space Weather - Critical Environmental Data */}
        <div style={{
          background: '#12141f',
          border: '1px solid #1e2235',
          borderRadius: 8,
          padding: 20,
          marginBottom: 24
        }}>
          <SpaceWeatherChart />
        </div>

        {/* Main Grid - 2 columns IBM style */}
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

        {/* Mitigation */}
        <div style={{
          background: '#12141f',
          border: '1px solid #1e2235',
          borderRadius: 8,
          padding: 20,
          marginBottom: 24
        }}>
          <MitigationChart />
        </div>

        {/* Footer - Professional */}
        <div style={{
          borderTop: '1px solid #1e2235',
          paddingTop: 16,
          marginTop: 32,
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <div style={{ fontSize: 11, color: '#6f6f6f' }}>
            QuantumPilot AI • IBM Quantum Live Data • 8.04M Calibration Records • NeuralUCB 22-D Context
          </div>
          <div style={{ fontSize: 11, color: '#6f6f6f' }}>
            github.com/ahmedzogly/QuantumPilot-AI • Apache 2.0
          </div>
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
