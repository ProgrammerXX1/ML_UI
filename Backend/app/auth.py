from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.user import UserRegister, UserLogin, Token
from services.user import create_user, authenticate_user
from core.security import create_access_token
from core.dependencies import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    user = create_user(db, user_data.username, user_data.password, user_data.is_api_user)
    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(401, "Invalid credentials")
    token = create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": token,
        "token_type": "bearer",  # ✅ добавили тип токена
        "username": user.username  # ✅ добавили имя пользователя
    }

