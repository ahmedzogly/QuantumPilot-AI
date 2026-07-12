import { useEffect, useState } from 'react'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function MitigationChart() {
  const [data, setData] = useState([])
  useEffect(() => {
    fetch('/mitigation_comparison.json').then(r=>r.json()).then(setData)
  }, [])
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>Mitigation Factory Comparison - S-ZNE 1.2x vs ZNE 5x Constant Overhead Advantage</h3>
      <ResponsiveContainer>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="method" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey="mitigated" fill="#00ff00" name="Mitigated Value" />
          <Bar dataKey="overhead" fill="#ff0000" name="Overhead x" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
