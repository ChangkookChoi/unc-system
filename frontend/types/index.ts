export interface MemberSummary {
  member_id: number
  member_name: string
  total: number
  done: number
  rate: number
  submitted: boolean
}

export interface DailyReport {
  report_date: string
  members: MemberSummary[]
  team_avg: number
}

export interface WeeklyReport {
  year: number
  week: number
  days: DailyReport[]
}

export interface StreakResult {
  member_id: number
  task_name: string | null
  streak: number
  latest_date: string | null
}

export interface CategoryStat {
  category: string
  total: number
  done: number
  rate: number
}
