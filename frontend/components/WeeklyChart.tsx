'use client'

import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts'
import type { WeeklyReport } from '@/types'

interface WeeklyChartProps {
  data: WeeklyReport
}

const COLORS = ['#6366f1', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899']

export default function WeeklyChart({ data }: WeeklyChartProps) {
  // 멤버 목록 (첫째 날 기준)
  const members = data.days[0]?.members.map((m) => m.member_name) ?? []

  // 차트 데이터: 날짜별 멤버별 달성률
  const chartData = data.days.map((day) => {
    const d = new Date(day.report_date)
    const label = `${d.getMonth() + 1}/${d.getDate()}`
    const entry: Record<string, string | number> = { date: label }
    day.members.forEach((m) => {
      entry[m.member_name] = m.submitted && m.total > 0
        ? Math.round(m.rate * 100)
        : 0
    })
    return entry
  })

  return (
    <ResponsiveContainer width="100%" height={240}>
      <LineChart data={chartData} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
        <XAxis dataKey="date" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} unit="%" />
        <Tooltip formatter={(v) => [`${v}%`]} />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        {members.map((name, i) => (
          <Line
            key={name}
            type="monotone"
            dataKey={name}
            stroke={COLORS[i % COLORS.length]}
            strokeWidth={2}
            dot={{ r: 3 }}
            connectNulls
          />
        ))}
      </LineChart>
    </ResponsiveContainer>
  )
}
