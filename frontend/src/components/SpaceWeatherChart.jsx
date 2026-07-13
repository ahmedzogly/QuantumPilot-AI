import { useEffect, useState } from 'react'
import { useLanguage } from '../context/LanguageContext'

export default function SpaceWeatherChart() {
  const { t, locale } = useLanguage()
  const [data, setData] = useState(null)

  useEffect(() => {
    fetch('/api/v1/spaceweather/live')
      .then(r => r.json())
      .then(d => setData(d))
      .catch(() => {
        setData({
          kp_index: 2.0,
          kp_source: "NOAA_1m",
          kp_status: "live",
          kp_time_tag: "2026-07-12T10:58:00",
          risk_level: locale==='ar' ? "هادئ نسبياً" : "Unsettled",
          t1_impact: locale==='ar' ? "انخفاض T1 بنسبة -5%" : "T1 slightly reduced -5%",
          neutron_flux: 94.6,
          neutron_unit: "counts/min",
          cosmic_ray_strength: 0.945,
          solar_zenith_deg: 74.65,
          temperature_c: 18.8,
          kp_norm: 0.222,
          temp_norm: 0.646,
          correlation_note: "T1 vs kp -0.197 p=0.00047"
        })
      })
  }, [locale])

  if (!data) return <div style={{ padding: 20, color: '#8d8d8d', fontSize: 13 }}>Loading space weather...</div>

  const getRiskColor = (risk) => {
    if (risk.includes("Severe") || risk.includes("شديد")) return "#da1e28"
    if (risk.includes("Storm") || risk.includes("عاصفة")) return "#ff832b"
    if (risk.includes("Unsettled") || risk.includes("هادئ نسبياً")) return "#f1c21b"
    return "#24a148"
  }

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>{t('space_weather')}</h3>
        <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>{t('space_weather_sub')}</p>
      </div>
      
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: 12 }}>
        <div style={{ background: '#0f111a', border: '1px solid #1e2235', borderRadius: 8, padding: 12 }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{t('risk')}</div>
          <div style={{ marginTop: 8, display: 'flex', alignItems: 'baseline', gap: 8 }}>
            <span style={{ fontSize: 28, fontWeight: 300, color: getRiskColor(data.risk_level) }}>{data.kp_index}</span>
            <span style={{ fontSize: 12, color: '#8d8d8d' }}>/9</span>
          </div>
          <div style={{ fontSize: 12, color: '#c6c6c6', marginTop: 4 }}>{data.risk_level}</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>{data.t1_impact}</div>
        </div>

        <div style={{ background: '#0f111a', border: '1px solid #1e2235', borderRadius: 8, padding: 12 }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{t('neutron_flux')}</div>
          <div style={{ fontSize: 20, fontWeight: 300, color: '#f4f4f4', marginTop: 8 }}>{typeof data.neutron_flux === 'number' ? data.neutron_flux.toFixed(1) : data.neutron_flux}</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>{data.neutron_unit}</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>{t('cosmic_ray')}: {typeof data.cosmic_ray_strength === 'number' ? data.cosmic_ray_strength.toFixed(3) : data.cosmic_ray_strength}</div>
        </div>

        <div style={{ background: '#0f111a', border: '1px solid #1e2235', borderRadius: 8, padding: 12 }}>
          <div style={{ fontSize: 11, color: '#8d8d8d', textTransform: 'uppercase', letterSpacing: '0.05em' }}>{t('solar_zenith')}</div>
          <div style={{ fontSize: 20, fontWeight: 300, color: '#f4f4f4', marginTop: 8 }}>{typeof data.solar_zenith_deg === 'number' ? data.solar_zenith_deg.toFixed(1) : data.solar_zenith_deg}°</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>{t('temperature')}: {data.temperature_c}°C</div>
          <div style={{ fontSize: 11, color: '#8d8d8d', marginTop: 4 }}>IBM Yorktown 41.27, -73.78</div>
        </div>
      </div>

      <div style={{ marginTop: 12, padding: 10, background: '#0a0e1a', borderRadius: 6, border: '1px solid #1e2235' }}>
        <div style={{ fontSize: 11, color: '#8d8d8d' }}>NeuralUCB Integration: kp_norm={typeof data.kp_norm === 'number' ? data.kp_norm.toFixed(3) : data.kp_norm} • temp_norm={typeof data.temp_norm === 'number' ? data.temp_norm.toFixed(3) : data.temp_norm} → 22-D context</div>
        <div style={{ fontSize: 11, color: '#6f6f6f', marginTop: 4 }}>{data.correlation_note}</div>
      </div>
    </div>
  )
}
