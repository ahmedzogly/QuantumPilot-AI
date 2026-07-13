import { useLanguage } from '../context/LanguageContext'

export default function Header() {
  const { locale, toggleLocale, t } = useLanguage()
  
  return (
    <header style={{
      background: 'linear-gradient(180deg, #0f111a 0%, #12141f 100%)',
      borderBottom: '1px solid #1e2235',
      padding: '16px 32px',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
      position: 'sticky',
      top: 0,
      zIndex: 100,
      backdropFilter: 'blur(20px)'
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
        <div style={{
          width: 36,
          height: 36,
          background: '#0f62fe',
          borderRadius: 6,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 600,
          fontSize: 16,
          color: 'white',
          letterSpacing: '-0.02em'
        }}>
          Q
        </div>
        <div>
          <h1 style={{ fontSize: 16, fontWeight: 600, color: '#f4f4f4', margin: 0, letterSpacing: '-0.01em', lineHeight: 1.2 }}>
            {t('title')}
          </h1>
          <p style={{ fontSize: 12, color: '#8d8d8d', margin: 0, fontWeight: 400, letterSpacing: '0.01em' }}>
            {t('subtitle')}
          </p>
        </div>
        <div style={{
          marginLeft: 24,
          padding: '4px 10px',
          background: 'rgba(15, 98, 254, 0.1)',
          border: '1px solid rgba(15, 98, 254, 0.2)',
          borderRadius: 16,
          fontSize: 10,
          color: '#0f62fe',
          fontWeight: 500,
          letterSpacing: '0.05em',
          textTransform: 'uppercase'
        }}>
          {t('ibm_quantum')} • {t('live')}
        </div>
      </div>
      
      <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
        <button
          onClick={toggleLocale}
          style={{
            padding: '8px 14px',
            background: '#212131',
            color: '#c6c6c6',
            border: '1px solid #2d2d44',
            borderRadius: 6,
            fontSize: 13,
            fontWeight: 400,
            cursor: 'pointer',
            transition: 'all 0.15s',
            display: 'flex',
            alignItems: 'center',
            gap: 6
          }}
        >
          <span style={{ fontSize: 14 }}>🌐</span>
          {t('language')}
        </button>
      </div>
    </header>
  )
}
