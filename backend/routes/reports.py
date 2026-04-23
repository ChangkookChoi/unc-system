from fastapi import APIRouter
from datetime import date

router = APIRouter()


@router.get("/reports/daily")
async def get_daily_report(target_date: date | None = None):
    """일간 달성 현황 (구현 예정)."""
    return {"date": target_date or date.today(), "members": []}
