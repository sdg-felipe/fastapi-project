from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from jose import jwt
from sqlalchemy.orm import Session
from core.config import JWT_SECRET, JWT_ALGORITHM
from models.auth import UserModel

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def auth_user(db: Session, username: str, password: str):
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not bcrypt_context.verify(password, user.password):
        return None
    return user

def create_access_token(id: int, username: str, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    encode = {
        "username": username,
        "id": id,
        "expires": expire.isoformat()
    }
    return jwt.encode(
        encode,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )
