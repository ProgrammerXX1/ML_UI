from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ChatLogItem(BaseModel):
    request_text: str
    response_text: str
    timestamp: datetime
    latency_ms: int
    chat_id: int

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=5000)
    title: Optional[str] = Field(None, max_length=100)

class ChatCreate(BaseModel):
    title: Optional[str] = Field("Новый чат", max_length=100)
    status: str = Field("Draft", max_length=20)

class ChatUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    status: Optional[str] = Field(None, max_length=20)

class ChatResponse(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True

class MessageResponse(BaseModel):
    request_text: str
    response_text: str
    timestamp: datetime
    latency_ms: int
    chat_id: int

    class Config:
        orm_mode = True

class ChatOut(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True

class ChatHistoryItem(BaseModel):
    question: str
    answer: str
