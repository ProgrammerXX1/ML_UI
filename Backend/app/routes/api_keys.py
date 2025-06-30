# routes/api_keys.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import APIKey
from core.dependencies import get_db, get_current_user
from schemas.api_keys import APIKeyOut
import secrets
from datetime import datetime

router = APIRouter()

@router.get("/api/keys/list", response_model=list[APIKeyOut])
def list_api_keys(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(APIKey).filter(APIKey.user_id == user.id).order_by(APIKey.created_at.desc()).all()

@router.post("/api/keys/create", response_model=APIKeyOut)
def create_api_key(db: Session = Depends(get_db), user=Depends(get_current_user)):
    new_key = secrets.token_hex(32)
    api_key = APIKey(user_id=user.id, key=new_key)
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key

@router.delete("/api/keys/{id}", status_code=204)
def delete_api_key(id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    key = db.query(APIKey).filter(APIKey.id == id, APIKey.user_id == user.id).first()
    if not key:
        raise HTTPException(status_code=404, detail="API-ключ не найден")
    db.delete(key)
    db.commit()
