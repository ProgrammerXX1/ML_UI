from pydantic import BaseModel
from datetime import datetime

class ChatLogItem(BaseModel):
    request_text: str
    response_text: str
    timestamp: datetime
    latency_ms: int
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class ChatHistoryItem(BaseModel):
    question: str
    answer: str