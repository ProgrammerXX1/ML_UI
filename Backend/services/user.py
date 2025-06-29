from sqlalchemy.orm import Session
from db.models import User
from core.security import hash_password, verify_password
import secrets

def create_user(db: Session, username: str, password: str, is_api_user: bool = False):
    hashed = hash_password(password)
    api_key = secrets.token_hex(32) if is_api_user else None
    user = User(username=username, hashed_password=hashed, is_api_user=is_api_user, api_key=api_key)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    print(f"🔍 Найден пользователь: {user.username}")
    print(f"🔐 Хеш в БД: {user.hashed_password}")
    print(f"🔑 Пароль введён: {password}")
    print(f"✅ Пароль совпадает? {verify_password(password, user.hashed_password)}")

    return user
