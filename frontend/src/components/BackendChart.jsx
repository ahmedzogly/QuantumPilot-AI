import { useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useLanguage } from '../context/LanguageContext'

export default function BackendChart() {
  const { t } = useLanguage()
  const [data] = useState([
    {name:'ibm_fez', T1:135.6, T2:106.3, RO:2.23, CZ:3.33},
    {name:'ibm_marrakesh', T1:170.9, T2:100.4, RO:2.73, CZ:4.52},
    {name:'ibm_kingston', T1:231, T2:159.7, RO:2.18, CZ:2.92}
  ])
  return (
    <div style={{ width: '100%' }}>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>{t('backends')}</h3>
        <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>{t('backends_sub')}</p>
      </div>
      <div style={{ width: '100%', height: 260 }}>
        <ResponsiveContainer>
          <BarChart data={data} barGap={8}>
            <CartesianGrid stroke="#1e2235" strokeDasharray="0" vertical={false} />
            <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#8d8d8d' }} axisLine={false} tickLine={false} />
            <YAxis tick={{ fontSize: 11, fill: '#8d8d8d' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ background: '#12141f', border: '1px solid #1e2235', borderRadius: 6, fontSize: 12 }} />
            <Legend wrapperStyle={{ fontSize: 11, color: '#8d8d8d' }} />
            <Bar dataKey="T1" fill="#0f62fe" name="T1 (µs)" radius={[2,2,0,0]} barSize={20} />
            <Bar dataKey="T2" fill="#8a3ffc" name="T2 (µs)" radius={[2,2,0,0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
