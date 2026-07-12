import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function TrainingChart() {
  const [data, setData] = useState<any[]>([])
  useEffect(() => {
    fetch('/training_history.json').then(r=>r.json()).then(setData)
  }, [])
  return (
    <div style={{ width: '100%', height: 250 }}>
      <h3>NeuralUCB Training - 8847 Real Contexts from 8M Drift</h3>
      <ResponsiveContainer>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis dataKey="epoch" />
          <YAxis domain={[0,0.4]} />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="train_loss" stroke="#8884d8" name="Train Loss 0.3224→0.0028" />
          <Line type="monotone" dataKey="val_loss" stroke="#82ca9d" name="Val Loss" />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
