"""APScheduler 기반 리마인더 스케줄러."""
import logging
from datetime import date
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from notifier import build_morning_reminder, build_evening_summary

logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler(timezone="Asia/Seoul")


async def _send_morning_reminder():
    msg = await build_morning_reminder()
    logger.info("아침 리마인더 발송:\n%s", msg)
    # TODO: 채널톡 연동 후 활성화
    # await channel_client.send_message(WORK_REPORT_CHANNEL_ID, msg)


async def _send_evening_summary():
    msg = await build_evening_summary()
    logger.info("저녁 집계 발송:\n%s", msg)
    # TODO: 채널톡 연동 후 활성화
    # await channel_client.send_message(WORK_REPORT_CHANNEL_ID, msg)


def start():
    scheduler.add_job(
        _send_morning_reminder,
        CronTrigger(hour=9, minute=0, timezone="Asia/Seoul"),
        id="morning_reminder",
        replace_existing=True,
    )
    scheduler.add_job(
        _send_evening_summary,
        CronTrigger(hour=23, minute=0, timezone="Asia/Seoul"),
        id="evening_summary",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("스케줄러 시작 — 09:00 리마인더 / 23:00 집계 고지 (Asia/Seoul)")


def shutdown():
    scheduler.shutdown(wait=False)
    logger.info("스케줄러 종료")
