# routes/api_keys.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.models import APIKey
from core.dependencies import get_db, get_current_user
from schemas.api_keys import APIKeyOut
import secrets
from core.API_dependencies import get_api_user, require_roles
from typing import List
from db.models import User, UserRole

router = APIRouter()

@router.get("/api/keys/list", response_model=List[APIKeyOut])
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

@router.get("/jwt-protected")
async def jwt_protected_route(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "role": current_user.role  # обязательно возвращаем роль
    }

@router.get("/api-key-protected")
async def api_key_protected_route(current_user: User = Depends(get_api_user)):
    return {"username": current_user.username}

@router.get("/admin-dashboard")
async def admin_dashboard(current_user: User = Depends(require_roles(UserRole.admin))):
    # Здесь логика для админа: мониторинг, статистика
    return {"message": "Welcome to admin dashboard"}

@router.get("/api/data")
async def api_data(current_user=Depends(require_roles(UserRole.admin, UserRole.coder))):
    # Логика для админа и кодера
    return {"message": "Доступ к API"}

@router.get("/chat")
async def chat_access(current_user=Depends(require_roles(UserRole.admin, UserRole.coder, UserRole.user))):
    # Логика для всех пользователей с доступом к чату
    return {"message": "Доступ к чату"}

@router.get("/admin/dashboard")
async def admin_dashboard(current_user=Depends(require_roles(UserRole.admin))):
    # Логика для админа
    return {"message": "Добро пожаловать в админ-панель"}
