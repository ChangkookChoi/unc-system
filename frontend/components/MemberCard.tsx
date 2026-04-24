import type { MemberSummary } from '@/types'

interface MemberCardProps {
  member: MemberSummary
}

export default function MemberCard({ member }: MemberCardProps) {
  const { member_name, done, total, rate, submitted } = member

  if (!submitted) {
    return (
      <div className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-700 dark:bg-zinc-900">
        <p className="font-medium text-zinc-900 dark:text-zinc-50">{member_name}</p>
        <p className="mt-2 text-sm text-zinc-400">미제출 ⚠️</p>
      </div>
    )
  }

  const pct = Math.round(rate * 100)
  const barColor =
    rate >= 1 ? 'bg-emerald-500' : rate >= 0.5 ? 'bg-amber-400' : 'bg-red-400'

  return (
    <div className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-700 dark:bg-zinc-900">
      <div className="flex items-center justify-between">
        <p className="font-medium text-zinc-900 dark:text-zinc-50">{member_name}</p>
        <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
          {done}/{total} ({pct}%)
        </span>
      </div>

      {/* 달성률 바 */}
      <div className="mt-3 h-2 w-full rounded-full bg-zinc-100 dark:bg-zinc-800">
        <div
          className={`h-2 rounded-full transition-all ${barColor}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
