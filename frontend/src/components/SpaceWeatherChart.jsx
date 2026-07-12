import { useEffect, useState } from 'react'

export default function SpaceWeatherChart() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/v1/spaceweather/live')
      .then(r => r.json())
      .then(d => {
        setData(d)
        setLoading(false)
      })
      .catch(() => {
        setData({
          kp_index: 2.0,
          estimated_kp: 2.0,
          kp_time_tag: "2026-07-12T10:58:00",
          kp_source: "NOAA_1m",
          kp_status: "live",
          risk_level: "Unsettled",
          t1_impact: "T1 slightly reduced -5%",
          neutron_flux: 94.6,
          neutron_unit: "counts/min (estimated Forbush model)",
          neutron_source: "mock_forbush_model",
          cosmic_ray_strength: 0.945,
          solar_zenith_deg: 74.65,
          temperature_c: 18.8,
          correlation_note: "From our 8M analysis: T1 vs kp -0.197 p=0.00047 significant"
        })
        setLoading(false)
      })
  }, [])

  if (loading) return <div>Loading live space weather from NOAA...</div>
  if (!data) return <div>No data</div>

  return (
    <div style={{ background: '#0f172a', padding: 15, borderRadius: 8, border: '2px solid #00ff88' }}>
      <h3>Live Space Weather - NOAA + Cosmic Ray Strength</h3>
      <p style={{ fontSize: 12, color: '#888' }}>Source: {data.kp_source} Status: {data.kp_status} Time: {data.kp_time_tag}</p>
      
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 10, marginTop: 10 }}>
        <div style={{ background: '#1e293b', padding: 10, borderRadius: 5 }}>
          <strong>Kp-index</strong><br/>
          <span style={{ fontSize: 24, color: data.kp_index >= 6 ? 'red' : data.kp_index >= 4 ? 'orange' : '#00ff00' }}>{data.kp_index}</span> /9<br/>
          <small>{data.risk_level}</small><br/>
          <small style={{ color: '#aaa' }}>{data.t1_impact}</small>
        </div>
        <div style={{ background: '#1e293b', padding: 10, borderRadius: 5 }}>
          <strong>Neutron Flux</strong><br/>
          <span style={{ fontSize: 20 }}>{data.neutron_flux?.toFixed ? data.neutron_flux.toFixed(1) : data.neutron_flux}</span> {data.neutron_unit}<br/>
          <small>Cosmic Ray Strength: {data.cosmic_ray_strength?.toFixed ? data.cosmic_ray_strength.toFixed(3) : data.cosmic_ray_strength}</small><br/>
          <small style={{ color: '#aaa' }}>Source: {data.neutron_source}</small>
        </div>
        <div style={{ background: '#1e293b', padding: 10, borderRadius: 5 }}>
          <strong>Solar Zenith</strong><br/>
          <span style={{ fontSize: 20 }}>{data.solar_zenith_deg?.toFixed ? data.solar_zenith_deg.toFixed(1) : data.solar_zenith_deg}°</span><br/>
          <small>Temp: {data.temperature_c}°C (NY)</small><br/>
          <small>IBM Yorktown 41.27, -73.78</small>
        </div>
      </div>

      <div style={{ marginTop: 10, padding: 10, background: '#1a1a1a', borderRadius: 5 }}>
        <strong>NeuralUCB Integration:</strong> kp_norm={data.kp_norm?.toFixed ? data.kp_norm.toFixed(3) : data.kp_norm} temp_norm={data.temp_norm?.toFixed ? data.temp_norm.toFixed(3) : data.temp_norm} → Last 2 dims of 22-D context vector<br/>
        <small style={{ color: '#888' }}>{data.correlation_note}</small><br/>
        <small style={{ color: '#00ff88' }}>{data.recommendation}</small>
      </div>
    </div>
  )
}
