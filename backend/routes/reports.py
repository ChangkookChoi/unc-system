from fastapi import APIRouter, HTTPException
from datetime import date
from aggregator import get_daily_report, get_weekly_report, get_member_streak, get_category_stats

router = APIRouter(prefix="/reports")


@router.get("/daily")
async def daily_report(target_date: date | None = None):
    """일간 팀 달성 현황."""
    return await get_daily_report(target_date or date.today())


@router.get("/weekly")
async def weekly_report(year: int | None = None, week: int | None = None):
    """주간 일별 달성 현황 (ISO 주차 기준)."""
    today = date.today()
    y = year or today.isocalendar().year
    w = week or today.isocalendar().week
    days = await get_weekly_report(y, w)
    return {"year": y, "week": w, "days": days}


@router.get("/members/{member_id}/streak")
async def member_streak(member_id: int, task: str | None = None):
    """멤버 연속 달성일 (스트릭). task 파라미터로 특정 태스크 스트릭 조회 가능."""
    return await get_member_streak(member_id, task)


@router.get("/categories")
async def category_stats(target_date: date | None = None):
    """카테고리별 팀 달성 현황."""
    return await get_category_stats(target_date or date.today())
