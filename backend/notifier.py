"""저녁 집계 메시지 포맷터."""
from datetime import date
from aggregator import get_daily_report, get_member_streak
from database import get_pool


async def build_evening_summary(target_date: date | None = None) -> str:
    """23:00 팀챗 고지용 메시지를 생성한다."""
    d = target_date or date.today()
    report = await get_daily_report(d)

    lines: list[str] = []
    lines.append(f"📊 {d.strftime('%m.%d')} 팀 달성 현황 (23:00 기준)\n")

    # 멤버별 현황
    submitted = [m for m in report.members if m.submitted and m.total > 0]
    not_submitted = [m for m in report.members if not m.submitted]

    for m in submitted:
        bar = _rate_icon(m.rate)
        lines.append(f"{bar} {m.member_name:<8} {m.done}/{m.total}  {m.rate:.0%}")

    for m in not_submitted:
        lines.append(f"⚠️  {m.member_name:<8} 미제출")

    # 팀 평균
    lines.append(f"\n팀 평균: {report.team_avg:.0%}")

    # 오늘 최다 달성 멤버
    if submitted:
        top = max(submitted, key=lambda m: m.rate)
        if top.rate > 0:
            lines.append(f"오늘의 MVP: {top.member_name} 🏆")

    # 스트릭 강조 (공통 태스크 중 전원 달성 연속일)
    streak_msg = await _build_streak_highlight(d)
    if streak_msg:
        lines.append(f"\n{streak_msg}")

    # 미제출 독려
    if not_submitted:
        names = ", ".join(m.member_name for m in not_submitted)
        lines.append(f"\n{names} — 아직 보고 안 올라왔어요 👀")

    return "\n".join(lines)


async def build_morning_reminder(target_date: date | None = None) -> str:
    """09:00 아침 리마인더 메시지를 생성한다."""
    d = target_date or date.today()
    return (
        f"📋 {d.strftime('%m.%d')} 업무계획을 공유해주세요!\n"
        "형식: MM.DD 이름 업무계획\n"
        "• 태스크1\n"
        "• 태스크2"
    )


# ── 내부 헬퍼 ────────────────────────────────────────────────────

def _rate_icon(rate: float) -> str:
    if rate >= 1.0:
        return "✅"
    if rate >= 0.5:
        return "🔶"
    return "❌"


async def _build_streak_highlight(target_date: date) -> str:
    """전체 멤버가 3일 이상 연속 달성 중인 공통 태스크 스트릭 메시지 반환."""
    pool = await get_pool()

    # 최근 7일간 전 멤버가 공통으로 완료한 태스크명 조회
    rows = await pool.fetch(
        """
        SELECT t.raw_name, COUNT(DISTINCT r.member_id) AS member_cnt
        FROM reports r
        JOIN completions c ON c.report_id = r.id
        JOIN tasks t ON t.id = c.task_id
        WHERE r.report_date = $1
          AND r.report_type = 'report'
          AND c.is_done = TRUE
          AND c.is_comment = FALSE
        GROUP BY t.raw_name
        HAVING COUNT(DISTINCT r.member_id) >= 2
        ORDER BY member_cnt DESC
        LIMIT 3
        """,
        target_date,
    )

    if not rows:
        return ""

    highlights: list[str] = []
    for row in rows:
        task_name = row['raw_name']
        # 해당 태스크를 완료한 멤버들의 스트릭 중 최솟값 = 팀 공통 스트릭
        member_streaks = await pool.fetch(
            """
            SELECT DISTINCT r.member_id
            FROM reports r
            JOIN completions c ON c.report_id = r.id
            JOIN tasks t ON t.id = c.task_id
            WHERE r.report_date = $1
              AND r.report_type = 'report'
              AND t.raw_name = $2
              AND c.is_done = TRUE
            """,
            target_date, task_name,
        )
        streaks = []
        for mr in member_streaks:
            s = await get_member_streak(mr['member_id'], task_name)
            streaks.append(s['streak'])

        min_streak = min(streaks) if streaks else 0
        if min_streak >= 3:
            highlights.append(
                f"🔥 {task_name}: {len(member_streaks)}명 {min_streak}일 연속 달성 중!"
            )

    return "\n".join(highlights)
