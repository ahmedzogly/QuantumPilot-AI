import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function BackendChart() {
  const [data, setData] = useState<any[]>([
    {name:'ibm_fez', T1:135.6, T2:106.3, RO:2.23, CZ:3.33},
    {name:'ibm_marrakesh', T1:170.9, T2:100.4, RO:2.73, CZ:4.52},
    {name:'ibm_kingston', T1:231, T2:159.7, RO:2.18, CZ:2.92}
  ])
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>Live Backends - Pulled Today via CRN DIGI (156q Heron R2)</h3>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="T1" fill="#8884d8" name="T1 us" />
          <Bar dataKey="T2" fill="#82ca9d" name="T2 us" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
