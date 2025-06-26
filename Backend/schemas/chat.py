from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
class ChatLogItem(BaseModel):
    request_text: str
    response_text: str
    timestamp: datetime
    latency_ms: int
    chat_id: Optional[int]

    class Config:
        orm_mode = True

class ChatRequest(BaseModel):
    message: str = Field(..., max_length=5000)
    title: Optional[str] = Field(None, max_length=100)  # Для создания чата

class ChatHistoryItem(BaseModel):
    question: str
    answer: str

class ChatCreate(BaseModel):
    title: Optional[str] = "Новый чат"
    status: Optional[str] = "Draft"  # Статус по умолчанию

class ChatUpdate(BaseModel):
    title: str
    status: Optional[str] = "Draft"  # Можно указать статус при обновлении

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
    chat_id: Optional[int]

    class Config:
        orm_mode = True
class ChatOut(BaseModel):
    id: int
    title: str
    status: str
    created_at: datetime

    class Config:
        orm_mode = True