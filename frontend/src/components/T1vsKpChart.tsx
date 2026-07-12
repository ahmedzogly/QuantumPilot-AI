import { useEffect, useState } from 'react'
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'

export default function T1vsKpChart() {
  const [data, setData] = useState<any[]>([])
  useEffect(() => {
    fetch('/t1_vs_kp.json').then(r=>r.json()).then(d=>setData(d.filter((x:any)=>x.T1 && x.kp)))
  }, [])
  return (
    <div style={{ width: '100%', height: 300 }}>
      <h3>Novelty: T1 vs Kp-index (Geomagnetic Activity) - Space Weather Correlation</h3>
      <p style={{fontSize:12,color:'#888'}}>First study linking kp_index (solar storm) to qubit decoherence from phanerozoic 8M dataset</p>
      <ResponsiveContainer>
        <ScatterChart>
          <CartesianGrid stroke="#333" />
          <XAxis type="number" dataKey="kp" name="Kp-index" domain={[0,9]} />
          <YAxis type="number" dataKey="T1" name="T1 (us)" />
          <Tooltip cursor={{ strokeDasharray: '3 3' }} />
          <Scatter data={data} fill="#ff7300" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  )
}
