# schemas/api_keys.py
from pydantic import BaseModel
from datetime import datetime

class APIKeyOut(BaseModel):
    id: int
    key: str
    created_at: datetime

    class Config:
        orm_mode = True
