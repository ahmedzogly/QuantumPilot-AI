import { useLanguage } from '../context/LanguageContext'

export default function Header() {
  const { locale, toggleLocale, t } = useLanguage()
  
  return (
    <header style={{
      background: 'rgba(15, 17, 26, 0.85)',
      backdropFilter: 'blur(20px)',
      borderBottom: '1px solid #1e2235',
      padding: '14px 32px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      position: 'sticky',
      top: 0,
      zIndex: 100
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <img 
          src="/logo.png" 
          alt="QuantumPilot AI Logo" 
          style={{ 
            width: 40, 
            height: 40, 
            objectFit: 'contain',
            filter: 'drop-shadow(0 0 8px rgba(15, 98, 254, 0.3))'
          }} 
        />
        <div>
          <h1 style={{ fontSize: 16, fontWeight: 600, color: '#f4f4f4', margin: 0, letterSpacing: '-0.01em', lineHeight: 1.2 }}>
            {t('title')}
          </h1>
          <p style={{ fontSize: 11, color: '#8d8d8d', margin: 0, fontWeight: 400, letterSpacing: '0.01em' }}>
            {t('subtitle')}
          </p>
        </div>
        <div style={{
          marginLeft: 20,
          padding: '3px 8px',
          background: 'rgba(15, 98, 254, 0.1)',
          border: '1px solid rgba(15, 98, 254, 0.2)',
          borderRadius: 12,
          fontSize: 10,
          color: '#0f62fe',
          fontWeight: 500,
          letterSpacing: '0.04em',
          textTransform: 'uppercase'
        }}>
          {t('ibm_quantum')} • {t('live')}
        </div>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
        <button
          onClick={toggleLocale}
          style={{
            padding: '7px 14px',
            background: '#1a1a2e',
            color: '#c6c6c6',
            border: '1px solid #2a2a40',
            borderRadius: 6,
            fontSize: 12,
            fontWeight: 400,
            cursor: 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: 6
          }}
        >
          <span>🌐</span>
          {t('language')}
        </button>
      </div>
    </header>
  )
}
