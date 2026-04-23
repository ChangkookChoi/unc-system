from pydantic import BaseModel
from datetime import date, datetime
from typing import Any


# ── 채널톡 Webhook 수신 스키마 ──────────────────────────────────

class ChannelEntity(BaseModel):
    id: str
    name: str | None = None

class MessageContent(BaseModel):
    type: str          # "text" | "file" | ...
    value: str | None = None

class WebhookMessage(BaseModel):
    id: str
    channelId: str
    writerId: str
    personType: str    # "member" | "manager" | "bot"
    content: MessageContent | None = None
    createdAt: datetime

class WebhookPayload(BaseModel):
    event: str         # "message_created" 등
    entity: dict[str, Any]
    refers: dict[str, Any] | None = None


# ── 파서 결과 스키마 ─────────────────────────────────────────────

class TaskItem(BaseModel):
    raw_name: str      # 원본 태스크명 (기호 제거 전)
    clean_name: str    # 기호 제거 후 태스크명
    is_done: bool
    raw_status: str    # 원본 완료 표기 ("o", "✅", "했음" 등)

class ParseResult(BaseModel):
    member_name: str
    report_date: date
    report_type: str   # "plan" | "report"
    tasks: list[TaskItem]
    confidence: float  # 0.0 ~ 1.0 (규칙 기반 파싱 신뢰도)
    used_claude: bool  # Claude API 폴백 여부


# ── 대시보드 API 응답 스키마 ─────────────────────────────────────

class MemberSummary(BaseModel):
    member_id: int
    member_name: str
    total: int
    done: int
    rate: float        # done / total (0.0 ~ 1.0)
    submitted: bool

class DailyReport(BaseModel):
    report_date: date
    members: list[MemberSummary]
    team_avg: float
