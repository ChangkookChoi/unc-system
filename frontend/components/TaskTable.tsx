import type { CategoryStat } from '@/types'

interface TaskTableProps {
  stats: CategoryStat[]
}

export default function TaskTable({ stats }: TaskTableProps) {
  if (stats.length === 0) {
    return <p className="text-sm text-zinc-400">데이터가 없습니다</p>
  }

  return (
    <table className="w-full text-sm">
      <thead>
        <tr className="border-b border-zinc-200 text-left text-xs text-zinc-500 dark:border-zinc-700">
          <th className="pb-2 font-medium">카테고리</th>
          <th className="pb-2 font-medium text-right">완료</th>
          <th className="pb-2 font-medium text-right">달성률</th>
          <th className="pb-2 pl-4 font-medium">그래프</th>
        </tr>
      </thead>
      <tbody>
        {stats.map((s) => {
          const pct = Math.round(s.rate * 100)
          const barColor =
            pct >= 100 ? 'bg-emerald-500' : pct >= 50 ? 'bg-amber-400' : 'bg-red-400'
          return (
            <tr
              key={s.category}
              className="border-b border-zinc-100 dark:border-zinc-800"
            >
              <td className="py-2.5 font-medium text-zinc-800 dark:text-zinc-200">
                {s.category}
              </td>
              <td className="py-2.5 text-right text-zinc-500">
                {s.done}/{s.total}
              </td>
              <td className="py-2.5 text-right font-semibold text-zinc-700 dark:text-zinc-300">
                {pct}%
              </td>
              <td className="py-2.5 pl-4">
                <div className="h-1.5 w-24 rounded-full bg-zinc-100 dark:bg-zinc-800">
                  <div
                    className={`h-1.5 rounded-full ${barColor}`}
                    style={{ width: `${pct}%` }}
                  />
                </div>
              </td>
            </tr>
          )
        })}
      </tbody>
    </table>
  )
}
