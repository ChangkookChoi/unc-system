import logging
from datetime import date, timedelta
from models import ParseResult, DailyReport, MemberSummary
from database import get_pool
from categorizer import categorize

logger = logging.getLogger(__name__)


# ── DB 저장 ──────────────────────────────────────────────────────

async def save_parse_result(result: ParseResult) -> None:
    """파싱 결과를 DB에 저장한다."""
    pool = await get_pool()

    # 멤버 조회 (없으면 자동 생성)
    member = await pool.fetchrow(
        "SELECT id FROM members WHERE name = $1", result.member_name
    )
    if not member:
        member = await pool.fetchrow(
            "INSERT INTO members (name) VALUES ($1) RETURNING id",
            result.member_name,
        )
    member_id = member['id']

    # 리포트 레코드 생성/갱신
    report = await pool.fetchrow(
        """
        INSERT INTO reports (member_id, report_date, report_type, submitted, submitted_at)
        VALUES ($1, $2, $3, $4, NOW())
        ON CONFLICT (member_id, report_date, report_type)
        DO UPDATE SET submitted = EXCLUDED.submitted, submitted_at = EXCLUDED.submitted_at
        RETURNING id
        """,
        member_id,
        result.report_date,
        result.report_type,
        result.report_type == 'report',
    )
    report_id = report['id']

    # 업무보고일 때: 같은 날 업무계획 태스크명 로드 (코멘트 감지용)
    plan_task_names: set[str] = set()
    if result.report_type == 'report':
        plan_rows = await pool.fetch(
            """
            SELECT t.raw_name
            FROM reports r
            JOIN completions c ON c.report_id = r.id
            JOIN tasks t ON t.id = c.task_id
            WHERE r.member_id = $1
              AND r.report_date = $2
              AND r.report_type = 'plan'
            """,
            member_id, result.report_date,
        )
        plan_task_names = {r['raw_name'] for r in plan_rows}

    # 태스크별 저장
    for task in result.tasks:
        cat_id, _ = await categorize(task.clean_name)

        # 태스크 조회 또는 생성
        task_record = await pool.fetchrow(
            """
            INSERT INTO tasks (raw_name, category_id, member_id)
            VALUES ($1, $2, $3)
            ON CONFLICT (raw_name, member_id) DO UPDATE SET category_id = EXCLUDED.category_id
            RETURNING id
            """,
            task.clean_name, cat_id, member_id,
        )
        task_id = task_record['id']

        # 계획에 없던 항목이면 코멘트로 표시
        is_comment = (
            result.report_type == 'report'
            and bool(plan_task_names)
            and task.clean_name not in plan_task_names
        )

        await pool.execute(
            """
            INSERT INTO completions (report_id, task_id, is_done, raw_status, is_comment)
            VALUES ($1, $2, $3, $4, $5)
            ON CONFLICT (report_id, task_id)
            DO UPDATE SET is_done = EXCLUDED.is_done, raw_status = EXCLUDED.raw_status
            """,
            report_id, task_id, task.is_done, task.raw_status, is_comment,
        )

    logger.info(
        "저장 완료: %s %s %s — %d개 태스크",
        result.report_date, result.member_name, result.report_type, len(result.tasks),
    )


# ── 집계 쿼리 ────────────────────────────────────────────────────

async def get_daily_report(target_date: date) -> DailyReport:
    """특정 날짜의 팀 전체 달성 현황을 반환한다."""
    pool = await get_pool()

    rows = await pool.fetch(
        """
        SELECT
            m.id                                          AS member_id,
            m.name                                        AS member_name,
            COALESCE(r.submitted, FALSE)                  AS submitted,
            COUNT(c.id)                                   AS total,
            COALESCE(SUM(CASE WHEN c.is_done THEN 1 ELSE 0 END), 0) AS done
        FROM members m
        LEFT JOIN reports r
            ON r.member_id = m.id
           AND r.report_date = $1
           AND r.report_type = 'report'
        LEFT JOIN completions c
            ON c.report_id = r.id
           AND c.is_comment = FALSE
        GROUP BY m.id, m.name, r.submitted
        ORDER BY m.id
        """,
        target_date,
    )

    members = [
        MemberSummary(
            member_id=r['member_id'],
            member_name=r['member_name'],
            total=r['total'],
            done=r['done'],
            rate=round(r['done'] / r['total'], 3) if r['total'] > 0 else 0.0,
            submitted=r['submitted'],
        )
        for r in rows
    ]

    submitted = [m for m in members if m.submitted and m.total > 0]
    team_avg = (
        round(sum(m.rate for m in submitted) / len(submitted), 3)
        if submitted else 0.0
    )

    return DailyReport(report_date=target_date, members=members, team_avg=team_avg)


async def get_weekly_report(year: int, week: int) -> list[DailyReport]:
    """주간 일별 달성 현황 리스트를 반환한다."""
    monday = date.fromisocalendar(year, week, 1)
    return [
        await get_daily_report(monday + timedelta(days=i))
        for i in range(7)
    ]


async def get_member_streak(member_id: int, task_name: str | None = None) -> dict:
    """
    멤버의 연속 달성일(스트릭)을 계산한다.

    - task_name 없음: 당일 태스크를 1개 이상 완료한 날 기준
    - task_name 있음: 해당 태스크를 완료한 날 기준
    """
    pool = await get_pool()

    if task_name:
        rows = await pool.fetch(
            """
            SELECT DISTINCT r.report_date
            FROM reports r
            JOIN completions c ON c.report_id = r.id
            JOIN tasks t ON t.id = c.task_id
            WHERE r.member_id = $1
              AND r.report_type = 'report'
              AND t.raw_name = $2
              AND c.is_done = TRUE
            ORDER BY r.report_date DESC
            """,
            member_id, task_name,
        )
    else:
        rows = await pool.fetch(
            """
            SELECT DISTINCT r.report_date
            FROM reports r
            JOIN completions c ON c.report_id = r.id
            WHERE r.member_id = $1
              AND r.report_type = 'report'
              AND c.is_done = TRUE
              AND c.is_comment = FALSE
            ORDER BY r.report_date DESC
            """,
            member_id,
        )

    dates = [r['report_date'] for r in rows]

    # 오늘 또는 어제부터 연속 계산
    streak = 0
    if dates:
        today = date.today()
        check = dates[0]
        # 가장 최근 날이 오늘 또는 어제여야 현재 스트릭으로 인정
        if check >= today - timedelta(days=1):
            for i, d in enumerate(dates):
                expected = check - timedelta(days=i)
                if d == expected:
                    streak += 1
                else:
                    break

    return {
        "member_id": member_id,
        "task_name": task_name,
        "streak": streak,
        "latest_date": dates[0].isoformat() if dates else None,
    }


async def get_category_stats(target_date: date) -> list[dict]:
    """날짜별 카테고리별 팀 달성 현황을 반환한다."""
    pool = await get_pool()
    rows = await pool.fetch(
        """
        SELECT
            c.name                                                   AS category,
            COUNT(comp.id)                                           AS total,
            COALESCE(SUM(CASE WHEN comp.is_done THEN 1 ELSE 0 END), 0) AS done
        FROM categories c
        JOIN tasks t ON t.category_id = c.id
        JOIN completions comp ON comp.task_id = t.id
        JOIN reports r ON r.id = comp.report_id
        WHERE r.report_date = $1
          AND r.report_type = 'report'
          AND comp.is_comment = FALSE
        GROUP BY c.name
        ORDER BY done DESC
        """,
        target_date,
    )
    return [
        {
            "category": r['category'],
            "total": r['total'],
            "done": r['done'],
            "rate": round(r['done'] / r['total'], 3) if r['total'] > 0 else 0.0,
        }
        for r in rows
    ]
