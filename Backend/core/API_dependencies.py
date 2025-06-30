from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models import User,APIKey
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_user(
    api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
) -> User:
    api_key_obj = db.query(APIKey).filter(APIKey.key == api_key).first()
    if not api_key_obj:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Invalid API key")
    user = db.query(User).filter(User.id == api_key_obj.user_id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
    return user
