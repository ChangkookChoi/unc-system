from fastapi import APIRouter, Request, HTTPException
from models import WebhookPayload

router = APIRouter()


@router.post("/webhook")
async def receive_webhook(request: Request):
    """채널톡 Webhook 수신 엔드포인트 (구현 예정)."""
    body = await request.json()
    return {"status": "ok"}
