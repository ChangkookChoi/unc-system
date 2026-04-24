import { Suspense } from 'react'
import { api } from '@/lib/api'
import StatCard from '@/components/StatCard'
import MemberCard from '@/components/MemberCard'
import AchievementChart from '@/components/AchievementChart'
import TaskTable from '@/components/TaskTable'

export default async function DashboardPage() {
  const today = new Date().toISOString().slice(0, 10)

  // 서버에서 병렬 데이터 페칭
  const [daily, categories] = await Promise.all([
    api.daily(today).catch(() => null),
    api.categories(today).catch(() => []),
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
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
          <h1 className="text-lg font-bold text-zinc-900 dark:text-zinc-50">unc-system</h1>
          <span className="text-sm text-zinc-500">{today}</span>
        </div>
      </header>

      <main className="mx-auto max-w-5xl space-y-8 px-6 py-8">
        {/* 오류 상태 */}
        {!daily && (
          <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-600">
            백엔드 서버에 연결할 수 없습니다. <code>uvicorn main:app --reload --port 8000</code> 확인해주세요.
          </div>
        )}

        {/* 지표 카드 */}
        <section className="grid grid-cols-2 gap-4 sm:grid-cols-4">
          <StatCard
            label="팀 평균 달성률"
            value={daily ? `${Math.round((daily.team_avg ?? 0) * 100)}%` : '-'}
          />
          <StatCard
            label="오늘 제출"
            value={`${submitted.length} / ${daily?.members.length ?? 0}`}
            sub="명 제출 완료"
          />
          <StatCard
            label="MVP"
            value={mvp ? mvp.member_name : '-'}
            sub={mvp ? `${Math.round(mvp.rate * 100)}% 달성` : undefined}
          />
          <StatCard
            label="미제출"
            value={notSubmitted.length > 0 ? `${notSubmitted.map((m) => m.member_name).join(', ')}` : '없음 🎉'}
          />
        </section>

        {/* 멤버 카드 */}
        {daily && (
          <section>
            <h2 className="mb-3 text-sm font-semibold text-zinc-500 dark:text-zinc-400">
              오늘 현황
            </h2>
            <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
              {daily.members.map((m) => (
                <MemberCard key={m.member_id} member={m} />
              ))}
            </div>
          </section>
        )}

        {/* 달성률 차트 + 카테고리 테이블 */}
        {daily && (
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
              <TaskTable stats={categories} />
            </section>
          </div>
        )}
      </main>
    </div>
  )
}
