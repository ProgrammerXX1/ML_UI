from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import time

from services.ml import generate_response
from db.models import Chat, ChatLog
from core.dependencies import get_db, get_current_user, get_api_user
from schemas.chat import (
    ChatRequest, ChatResponse, ChatLogItem,
    ChatCreate, ChatOut, ChatUpdate, MessageResponse
)
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
router = APIRouter()

# Отправка сообщения в чат (создаёт чат, если не указан chat_id или чат не существует)
@router.post("/chat", response_model=MessageResponse)
def send_message(
    request: ChatRequest,
    chat_id: Optional[int] = None,  # chat_id необязательный
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    # Если chat_id указан, проверяем существование чата
    if chat_id:
        chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
        if not chat:
            raise HTTPException(status_code=404, detail="Чат не найден")
    else:
        # Создаём новый чат, если chat_id не указан
        chat = Chat(user_id=user.id, title=request.title or "Новый чат", status="Draft")
        db.add(chat)
        db.commit()
        db.refresh(chat)
        chat_id = chat.id

    # Генерируем ответ от ML
    start = time.time()
    try:
        response = generate_response(request.message)
    except Exception as e:
        log = ChatLog(
            user_id=user.id,
            chat_id=chat_id,
            api_key=user.api_key,
            request_text=request.message,
            response_text=str(e),
            status="error",
            latency_ms=int((time.time() - start) * 1000)
        )
        db.add(log)
        db.commit()
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

    # Сохраняем сообщение
    log = ChatLog(
        user_id=user.id,
        chat_id=chat_id,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response,
        status="success",
        latency_ms=int((time.time() - start) * 1000)
    )
    db.add(log)
    db.commit()

    return MessageResponse(
        request_text=log.request_text,
        response_text=log.response_text,
        timestamp=log.timestamp,
        latency_ms=log.latency_ms,
        chat_id=chat_id
    )
# API для внешних клиентов (без привязки к чату)
@router.post("/api", response_model=ChatResponse)
def chat_api(request: ChatRequest, db: Session = Depends(get_db), user=Depends(get_api_user)):
    start = time.time()
    try:
        response = generate_response(request.message)
    except Exception as e:
        log = ChatLog(
            user_id=user.id,
            api_key=user.api_key,
            request_text=request.message,
            response_text=str(e),
            status="error",
            latency_ms=int((time.time() - start) * 1000)
        )
        db.add(log)
        db.commit()
        raise HTTPException(status_code=500, detail="Ошибка генерации ответа")

    log = ChatLog(
        user_id=user.id,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response,
        status="success",
        latency_ms=int((time.time() - start) * 1000)
    )
    db.add(log)
    db.commit()

    return {"response": response}
# История сообщений пользователя (все чаты)
@router.get("/history", response_model=List[ChatLogItem])
def get_user_chat_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    logs = db.query(ChatLog)\
        .filter(ChatLog.user_id == user.id)\
        .order_by(ChatLog.timestamp.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

    return [
        ChatLogItem(
            request_text=log.request_text,
            response_text=log.response_text,
            timestamp=log.timestamp,
            latency_ms=log.latency_ms,
            chat_id=log.chat_id
        ) for log in logs
    ]
# История сообщений API
@router.get("api/history", response_model=List[ChatLogItem])
def get_api_chat_history(
    db: Session = Depends(get_db),
    user=Depends(get_api_user),
    limit: int = 20,
    offset: int = 0
):
    logs = db.query(ChatLog)\
        .filter(ChatLog.api_key == user.api_key)\
        .order_by(ChatLog.timestamp.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

    return [
        ChatLogItem(
            request_text=log.request_text,
            response_text=log.response_text,
            timestamp=log.timestamp,
            latency_ms=log.latency_ms,
            chat_id=log.chat_id
        ) for log in logs
    ]
# История сообщений конкретного чата
@router.get("/history/{chat_id}", response_model=List[ChatLogItem])
def get_chat_history(
    chat_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    logs = db.query(ChatLog)\
        .filter(ChatLog.chat_id == chat_id, ChatLog.user_id == user.id)\
        .order_by(ChatLog.timestamp.desc())\
        .limit(limit)\
        .offset(offset)\
        .all()

    return [
        ChatLogItem(
            request_text=log.request_text,
            response_text=log.response_text,
            timestamp=log.timestamp,
            latency_ms=log.latency_ms,
            chat_id=log.chat_id
        ) for log in logs
    ]
# Создание чата
@router.post("/create", response_model=ChatOut)
def create_chat(chat: ChatCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_chat = Chat(user_id=user.id, title=chat.title or "Новый чат", status=chat.status or "Draft")
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat
# Получение сообщений чата
@router.get("/{chat_id}/messages", response_model=List[MessageResponse])
def get_chat_messages(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    return [
        MessageResponse(
            request_text=message.request_text,
            response_text=message.response_text,
            timestamp=message.timestamp,
            latency_ms=message.latency_ms,
            chat_id=message.chat_id
        ) for message in chat.messages
    ]
# Список чатов пользователя
@router.get("/list", response_model=List[ChatOut])
def get_chat_list(db: Session = Depends(get_db), user=Depends(get_current_user)):
    
    try:
        logger.info(f"Fetching chat list for user_id: {user.id}")
        chats = db.query(Chat).filter(Chat.user_id == user.id).order_by(Chat.created_at.desc()).all()
        logger.info(f"Found {len(chats)} chats: {[chat.__dict__ for chat in chats]}")
        return chats
    except Exception as e:
        logger.error(f"Error in get_chat_list: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
# Обновление названия чата
@router.patch("/{chat_id}", response_model=ChatOut)
def update_chat(chat_id: int, update: ChatUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    chat.title = update.title
    db.commit()
    return chat
@router.get("/{chat_id}", response_model=ChatOut)
def get_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    return chat
# Удаление чата
@router.delete("/{chat_id}", status_code=204)
def delete_chat(chat_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")
    db.delete(chat)
    db.commit()
    return
@router.post("/{chat_id}/save")
def save_chat_messages(
    chat_id: int,
    messages: List[MessageResponse],
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    chat = db.query(Chat).filter(Chat.id == chat_id, Chat.user_id == user.id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Чат не найден")

    # Очищаем существующие сообщения
    db.query(ChatLog).filter(ChatLog.chat_id == chat_id).delete()

    # Сохраняем новые сообщения
    for msg in messages:
        db_message = ChatLog(
            user_id=user.id,
            chat_id=chat_id,
            api_key=user.api_key,
            request_text=msg.request_text,
            response_text=msg.response_text,
            timestamp=msg.timestamp,
            latency_ms=msg.latency_ms
        )
        db.add(db_message)
    
    db.commit()
    return {"status": "success"}