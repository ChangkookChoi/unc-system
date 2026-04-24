import logging
from fastapi import APIRouter, Request, HTTPException
from parser import parse_message, detect_multi_block

logger = logging.getLogger(__name__)
router = APIRouter()

MULTI_BLOCK_NOTICE = (
    "날짜가 다른 내용은 메시지를 나눠서 보내주세요! 😊\n"
    "봇이 첫 번째 내용만 처리했어요.\n"
    "예) 04.01 보고 → 전송 → 04.02 계획 → 전송"
)


@router.post("/webhook")
async def receive_webhook(request: Request):
    """채널톡 Webhook 수신 엔드포인트."""
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    event = body.get("event", "")

    # message_created 이벤트만 처리
    if event != "message_created":
        return {"status": "ignored"}

    entity = body.get("entity", {})
    message_text = entity.get("content", {}).get("value", "") or ""
    member_name: str | None = None  # 채널톡 실제 유저명 (연동 완료 후 채움)

    if not message_text.strip():
        return {"status": "empty"}

    # 멀티 블록 감지 — 서버 뻗지 않게 예외처리
    if detect_multi_block(message_text):
        logger.warning("멀티 블록 메시지 감지: member=%s", member_name)
        # TODO: 채널톡 API 연동 후 MULTI_BLOCK_NOTICE 발송
        # await channel_client.send_message(channel_id, MULTI_BLOCK_NOTICE)
        logger.info("멀티 블록 안내 메시지 예정: %s", MULTI_BLOCK_NOTICE)
        # 첫 번째 블록만 파싱 진행 (아래 로직에서 자연스럽게 처리됨)

    result = parse_message(message_text, member_name=member_name)

    if result is None:
        return {"status": "not_a_report"}

    # TODO: DB 저장 (aggregator 구현 후 연결)
    logger.info(
        "파싱 완료: %s %s %s — %d개 태스크, 신뢰도 %.0f%%",
        result.report_date,
        result.member_name,
        result.report_type,
        len(result.tasks),
        result.confidence * 100,
    )

    return {"status": "ok", "parsed": result.model_dump()}
