from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
import time
import logging

from services.ml import generate_response
from db.models import Chat, ChatLog, User
from core.dependencies import get_db
from schemas.chat import (
    ChatRequest, MessageResponse
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api")  # ⬅️ Внешний префикс

# 🔐 Получение пользователя по api_key
def get_user_by_api_key(request: Request, db: Session):
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    user = db.query(User).filter(User.api_key == api_key).first()
    if not user:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return user

# ✅ Отправка запроса от внешнего API
@router.post("/chat/send", response_model=MessageResponse)
def api_send_message(request_data: ChatRequest, request: Request, db: Session = Depends(get_db)):
    user = get_user_by_api_key(request, db)

    start = time.time()
    try:
        response_text = generate_response(request_data.message)
    except Exception as e:
        logger.exception("❌ Ошибка генерации ответа")
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

    latency = int((time.time() - start) * 1000)

    log = ChatLog(
        user_id=user.id,
        chat_id=None,
        api_key=user.api_key,
        request_text=request_data.message,
        response_text=response_text,
        status="success",
        latency_ms=latency
    )
    db.add(log)
    db.commit()

    return MessageResponse(
        request_text=log.request_text,
        response_text=log.response_text,
        timestamp=log.timestamp,
        latency_ms=log.latency_ms,
        chat_id=None
    )
