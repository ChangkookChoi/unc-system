'use client'

import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts'
import type { MemberSummary } from '@/types'

interface AchievementChartProps {
  members: MemberSummary[]
}

export default function AchievementChart({ members }: AchievementChartProps) {
  const data = members
    .filter((m) => m.submitted && m.total > 0)
    .map((m) => ({
      name: m.member_name,
      rate: Math.round(m.rate * 100),
    }))

  if (data.length === 0) {
    return (
      <div className="flex h-40 items-center justify-center text-sm text-zinc-400">
        제출된 보고가 없습니다
      </div>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={200}>
      <BarChart data={data} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#e4e4e7" />
        <XAxis dataKey="name" tick={{ fontSize: 12 }} />
        <YAxis domain={[0, 100]} tick={{ fontSize: 12 }} unit="%" />
        <Tooltip formatter={(v: number) => `${v}%`} />
        <Bar dataKey="rate" radius={[4, 4, 0, 0]}>
          {data.map((entry) => (
            <Cell
              key={entry.name}
              fill={entry.rate >= 100 ? '#10b981' : entry.rate >= 50 ? '#f59e0b' : '#f87171'}
            />
          ))}
        </Bar>
      </BarChart>
    </ResponsiveContainer>
  )
}
