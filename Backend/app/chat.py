from fastapi import APIRouter, Depends
from schemas.chat import ChatRequest, ChatResponse, ChatLogItem
from services.ml import generate_response
from db.models import ChatLog
from core.dependencies import get_db, get_current_user, get_api_user
from sqlalchemy.orm import Session
import time
from typing import List

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    start = time.time()
    response = generate_response(request.message)
    latency = int((time.time() - start) * 1000)

    log = ChatLog(
        user_id=user.id,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response,
        status="success",
        latency_ms=latency
    )
    db.add(log)
    db.commit()

    return {"response": response}


@router.post("/api", response_model=ChatResponse)
def chat_api(
    request: ChatRequest,
    db: Session = Depends(get_db),
    user = Depends(get_api_user)
):
    start = time.time()
    response = generate_response(request.message)
    latency = int((time.time() - start) * 1000)

    log = ChatLog(
        user_id=user.id,
        api_key=user.api_key,
        request_text=request.message,
        response_text=response,
        status="success",
        latency_ms=latency
    )
    db.add(log)
    db.commit()

    return {"response": response}


@router.get("/chat/history", response_model=List[ChatLogItem])
def get_user_chat_history(
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):
    logs = db.query(ChatLog)\
        .filter(ChatLog.user_id == user.id)\
        .order_by(ChatLog.timestamp.desc())\
        .limit(20)\
        .all()

    return [
        ChatLogItem(
            request_text=log.request_text,
            response_text=log.response_text,
            timestamp=log.timestamp,
            latency_ms=log.latency_ms
        ) for log in logs
    ]


@router.get("/chat/api/history", response_model=List[ChatLogItem])
def get_api_chat_history(
    db: Session = Depends(get_db),
    user=Depends(get_api_user)
):
    logs = db.query(ChatLog)\
        .filter(ChatLog.api_key == user.api_key)\
        .order_by(ChatLog.timestamp.desc())\
        .limit(20)\
        .all()

    return [
        ChatLogItem(
            request_text=log.request_text,
            response_text=log.response_text,
            timestamp=log.timestamp,
            latency_ms=log.latency_ms
        ) for log in logs
    ]
