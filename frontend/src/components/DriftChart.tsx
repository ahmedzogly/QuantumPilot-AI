import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function DriftChart() {
  const [data, setData] = useState<any[]>([])
  useEffect(() => {
    fetch('/drift_timeseries.json').then(r=>r.json()).then(d=>setData(d.slice(0,50)))
  }, [])
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>T1 Drift vs Time (ibm_fez 156q - Live from 8M dataset)</h3>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="time" hide />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="T1_us" stroke="#00ff00" name="T1 (us)" dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
