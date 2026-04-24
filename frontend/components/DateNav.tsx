'use client'

import { useRouter, useSearchParams } from 'next/navigation'

interface DateNavProps {
  currentDate: string   // 'YYYY-MM-DD'
  currentView: 'daily' | 'weekly'
}

export default function DateNav({ currentDate, currentView }: DateNavProps) {
  const router = useRouter()
  const searchParams = useSearchParams()

  function navigate(date: string, view: string) {
    const params = new URLSearchParams(searchParams.toString())
    params.set('date', date)
    params.set('view', view)
    router.push(`?${params.toString()}`)
  }

  function shiftDate(days: number) {
    const d = new Date(currentDate)
    d.setDate(d.getDate() + days)
    navigate(d.toISOString().slice(0, 10), currentView)
  }

  function shiftWeek(weeks: number) {
    const d = new Date(currentDate)
    d.setDate(d.getDate() + weeks * 7)
    navigate(d.toISOString().slice(0, 10), 'weekly')
  }

  const isToday = currentDate === new Date().toISOString().slice(0, 10)

  return (
    <div className="flex items-center gap-3">
      {/* 뷰 토글 */}
      <div className="flex rounded-lg border border-zinc-200 dark:border-zinc-700 overflow-hidden text-sm">
        {(['daily', 'weekly'] as const).map((v) => (
          <button
            key={v}
            onClick={() => navigate(currentDate, v)}
            className={`px-3 py-1.5 transition-colors ${
              currentView === v
                ? 'bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900'
                : 'text-zinc-500 hover:bg-zinc-50 dark:hover:bg-zinc-800'
            }`}
          >
            {v === 'daily' ? '일간' : '주간'}
          </button>
        ))}
      </div>

      {/* 날짜 이동 */}
      <div className="flex items-center gap-1">
        <button
          onClick={() => currentView === 'daily' ? shiftDate(-1) : shiftWeek(-1)}
          className="rounded p-1.5 text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          aria-label="이전"
        >
          ‹
        </button>

        <span className="min-w-[7rem] text-center text-sm font-medium text-zinc-700 dark:text-zinc-300">
          {currentView === 'daily'
            ? formatDate(currentDate)
            : `${getWeekRange(currentDate)}`}
        </span>

        <button
          onClick={() => currentView === 'daily' ? shiftDate(1) : shiftWeek(1)}
          disabled={isToday && currentView === 'daily'}
          className="rounded p-1.5 text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800 disabled:opacity-30"
          aria-label="다음"
        >
          ›
        </button>
      </div>

      {/* 오늘로 */}
      {!isToday && (
        <button
          onClick={() => navigate(new Date().toISOString().slice(0, 10), currentView)}
          className="text-xs text-zinc-400 underline underline-offset-2 hover:text-zinc-600"
        >
          오늘
        </button>
      )}
    </div>
  )
}

function formatDate(iso: string) {
  const d = new Date(iso)
  return `${d.getMonth() + 1}/${d.getDate()} (${['일','월','화','수','목','금','토'][d.getDay()]})`
}

function getWeekRange(iso: string) {
  const d = new Date(iso)
  const day = d.getDay()
  const mon = new Date(d)
  mon.setDate(d.getDate() - (day === 0 ? 6 : day - 1))
  const sun = new Date(mon)
  sun.setDate(mon.getDate() + 6)
  return `${mon.getMonth()+1}/${mon.getDate()} – ${sun.getMonth()+1}/${sun.getDate()}`
}
