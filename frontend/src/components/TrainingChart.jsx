import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { useLanguage } from '../context/LanguageContext'

export default function TrainingChart() {
  const { t } = useLanguage()
  const [data, setData] = useState([])
  useEffect(() => {
    fetch('/training_history.json').then(r=>r.json()).then(setData).catch(()=>setData([
      {epoch:0,train_loss:0.3224,val_loss:0.0051},
      {epoch:10,train_loss:0.0034,val_loss:0.003},
      {epoch:30,train_loss:0.0055,val_loss:0.0032},
      {epoch:60,train_loss:0.0031,val_loss:0.0036},
      {epoch:90,train_loss:0.0028,val_loss:0.0029}
    ]))
  }, [])
  return (
    <div style={{ width: '100%' }}>
      <div style={{ marginBottom: 16 }}>
        <h3 style={{ fontSize: 14, fontWeight: 600, color: '#f4f4f4', margin: 0 }}>{t('training')}</h3>
        <p style={{ fontSize: 12, color: '#8d8d8d', margin: '4px 0 0 0' }}>{t('training_sub')}</p>
      </div>
      <div style={{ width: '100%', height: 220 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <CartesianGrid stroke="#1e2235" strokeDasharray="0" vertical={false} />
            <XAxis dataKey="epoch" tick={{ fontSize: 11, fill: '#8d8d8d' }} axisLine={false} tickLine={false} />
            <YAxis domain={[0,0.4]} tick={{ fontSize: 11, fill: '#8d8d8d' }} axisLine={false} tickLine={false} />
            <Tooltip contentStyle={{ background: '#12141f', border: '1px solid #1e2235', borderRadius: 6, fontSize: 12 }} />
            <Legend wrapperStyle={{ fontSize: 11 }} />
            <Line type="monotone" dataKey="train_loss" stroke="#0f62fe" strokeWidth={2} dot={false} name={t('loss') + ' Train'} />
            <Line type="monotone" dataKey="val_loss" stroke="#08bdba" strokeWidth={2} dot={false} name={t('loss') + ' Val'} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
