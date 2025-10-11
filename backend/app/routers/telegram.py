from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()

class WebhookUpdate(BaseModel):
    """Telegram webhook update model"""
    update_id: int
    message: Optional[dict] = None
    callback_query: Optional[dict] = None

@router.post("/webhook")
async def telegram_webhook(update: WebhookUpdate, background_tasks: BackgroundTasks):
    """
    Handle incoming Telegram webhook updates
    This endpoint receives updates from Telegram when users interact with the bot
    """
    try:
        # Process the update in the background
        # The actual bot application will handle this
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/subscribers/count")
async def get_subscriber_count():
    """Get the number of bot subscribers"""
    from app.services.telegram_bot import load_subscriptions
    subscriptions = load_subscriptions()
    return {"count": len(subscriptions)}

@router.get("/health")
async def telegram_health():
    """Check if Telegram bot is configured"""
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    return {
        "configured": bool(bot_token),
        "status": "ready" if bot_token else "not_configured"
    }
