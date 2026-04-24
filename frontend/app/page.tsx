import { Suspense } from 'react'
import { api } from '@/lib/api'
import StatCard from '@/components/StatCard'
import MemberCard from '@/components/MemberCard'
import AchievementChart from '@/components/AchievementChart'
import WeeklyChart from '@/components/WeeklyChart'
import TaskTable from '@/components/TaskTable'
import DateNav from '@/components/DateNav'

interface PageProps {
  searchParams: Promise<{ date?: string; view?: string }>
}

export default async function DashboardPage({ searchParams }: PageProps) {
  const { date, view } = await searchParams

  const today = new Date().toISOString().slice(0, 10)
  const currentDate = date ?? today
  const currentView = view === 'weekly' ? 'weekly' : 'daily'

  // ISO 주차 계산
  const d = new Date(currentDate)
  const iso = getISOWeek(d)

  // 데이터 페칭
  const [daily, weekly, categories] = await Promise.all([
    api.daily(currentDate).catch(() => null),
    currentView === 'weekly' ? api.weekly(iso.year, iso.week).catch(() => null) : null,
    currentView === 'daily' ? api.categories(currentDate).catch(() => []) : [],
  ])

  const submitted = daily?.members.filter((m) => m.submitted && m.total > 0) ?? []
  const notSubmitted = daily?.members.filter((m) => !m.submitted) ?? []
  const mvp = submitted.length > 0
    ? submitted.reduce((a, b) => (a.rate >= b.rate ? a : b))
    : null

  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-zinc-950">
      {/* 헤더 */}
      <header className="border-b border-zinc-200 bg-white dark:border-zinc-800 dark:bg-zinc-900">
        <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-3 px-6 py-4">
          <h1 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">unc-system</h1>
          <Suspense>
            <DateNav currentDate={currentDate} currentView={currentView} />
          </Suspense>
        </div>
      </header>

      <main className="mx-auto max-w-5xl space-y-8 px-6 py-8">
        {/* 백엔드 연결 오류 */}
        {!daily && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
            백엔드 서버에 연결할 수 없습니다.{' '}
            <code>uvicorn main:app --reload --port 8000</code> 확인해주세요.
          </div>
        )}

        {/* ── 일간 뷰 ── */}
        {currentView === 'daily' && daily && (
          <>
            {/* 지표 카드 */}
            <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
              <StatCard
                label="팀 평균 달성률"
                value={`${Math.round((daily.team_avg ?? 0) * 100)}%`}
              />
              <StatCard
                label="오늘 제출"
                value={`${submitted.length} / ${daily.members.length}`}
                sub="명 제출"
              />
              <StatCard
                label="MVP"
                value={mvp?.member_name ?? '-'}
                sub={mvp ? `${Math.round(mvp.rate * 100)}% 달성` : undefined}
              />
              <StatCard
                label="미제출"
                value={
                  notSubmitted.length > 0
                    ? notSubmitted.map((m) => m.member_name).join(', ')
                    : '없음 🎉'
                }
              />
            </section>

            {/* 멤버 카드 */}
            <section>
              <h2 className="mb-3 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
                멤버 현황
              </h2>
              <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
                {daily.members.map((m) => (
                  <MemberCard key={m.member_id} member={m} />
                ))}
              </div>
            </section>

            {/* 차트 + 카테고리 테이블 */}
            <div className="grid gap-6 lg:grid-cols-2">
              <section className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-700 dark:bg-zinc-900">
                <h2 className="mb-4 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
                  멤버별 달성률
                </h2>
                <Suspense fallback={<div className="h-48 animate-pulse rounded bg-zinc-100" />}>
                  <AchievementChart members={daily.members} />
                </Suspense>
              </section>

              <section className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-700 dark:bg-zinc-900">
                <h2 className="mb-4 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
                  카테고리별 달성
                </h2>
                <TaskTable stats={categories as any[]} />
              </section>
            </div>
          </>
        )}

        {/* ── 주간 뷰 ── */}
        {currentView === 'weekly' && (
          <>
            {weekly ? (
              <>
                {/* 주간 팀 평균 요약 */}
                <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
                  {weekly.days.slice(0, 4).map((day) => (
                    <StatCard
                      key={day.report_date}
                      label={formatShortDate(day.report_date)}
                      value={`${Math.round((day.team_avg ?? 0) * 100)}%`}
                      sub={`${day.members.filter((m) => m.submitted).length}명 제출`}
                    />
                  ))}
                </section>

                {/* 주간 라인 차트 */}
                <section className="rounded-xl border border-zinc-200 bg-white p-5 dark:border-zinc-700 dark:bg-zinc-900">
                  <h2 className="mb-4 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
                    주간 멤버별 달성 추이
                  </h2>
                  <Suspense fallback={<div className="h-56 animate-pulse rounded bg-zinc-100" />}>
                    <WeeklyChart data={weekly} />
                  </Suspense>
                </section>

                {/* 주간 일별 상세 */}
                <section>
                  <h2 className="mb-3 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
                    일별 상세
                  </h2>
                  <div className="space-y-2">
                    {weekly.days.map((day) => {
                      const sub = day.members.filter((m) => m.submitted && m.total > 0)
                      if (sub.length === 0) return null
                      return (
                        <div
                          key={day.report_date}
                          className="flex items-center gap-4 rounded-lg border border-zinc-100 bg-white px-4 py-3 dark:border-zinc-800 dark:bg-zinc-900"
                        >
                          <span className="w-16 shrink-0 text-sm font-medium text-zinc-500">
                            {formatShortDate(day.report_date)}
                          </span>
                          <div className="flex flex-1 flex-wrap gap-2">
                            {sub.map((m) => (
                              <span
                                key={m.member_id}
                                className="text-xs text-zinc-600 dark:text-zinc-400"
                              >
                                {m.member_name} {Math.round(m.rate * 100)}%
                              </span>
                            ))}
                          </div>
                          <span className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">
                            팀 {Math.round((day.team_avg ?? 0) * 100)}%
                          </span>
                        </div>
                      )
                    })}
                  </div>
                </section>
              </>
            ) : (
              <div className="rounded-xl border border-zinc-200 bg-white p-8 text-center text-sm text-zinc-400">
                이 주의 데이터가 없습니다
              </div>
            )}
          </>
        )}
      </main>
    </div>
  )
}

function formatShortDate(iso: string) {
  const d = new Date(iso)
  return `${d.getMonth() + 1}/${d.getDate()} (${['일','월','화','수','목','금','토'][d.getDay()]})`
}

function getISOWeek(d: Date) {
  const date = new Date(d)
  date.setHours(0, 0, 0, 0)
  date.setDate(date.getDate() + 3 - ((date.getDay() + 6) % 7))
  const week1 = new Date(date.getFullYear(), 0, 4)
  const week = Math.round(
    ((date.getTime() - week1.getTime()) / 86400000 - 3 + ((week1.getDay() + 6) % 7)) / 7
  ) + 1
  return { year: date.getFullYear(), week }
}
