from datetime import timedelta
from fastapi import APIRouter, HTTPException, Depends
from dependencies.auth import get_current_user
from dependencies.db import db_dependency
from fastapi.security import OAuth2PasswordRequestForm

from schemas.user import User, UserCreate
from services.auth_service import auth_user, create_access_token
from services.user_service import get_user_by_id, create_user, get_user_by_email, get_user_by_username

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

@router.get("/me", response_model=User)
async def get_user(db: db_dependency, current_user: User = Depends(get_current_user)):
    user = get_user_by_id(db, current_user.get("id"))
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user

@router.post("/token")
async def get_token(db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth_user(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token(user.id, user.username, timedelta(minutes=30))
    return {'access_token': token, 'token_type': 'bearer'}

@router.post("/register")
async def register(db: db_dependency, new_user: UserCreate):
    if get_user_by_email(db, new_user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if get_user_by_username(db, new_user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    from passlib.context import CryptContext
    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = bcrypt_context.hash(new_user.password)

    created_user = create_user(db, new_user.email, new_user.username, hashed_password, new_user.role,
                               new_user.phone_number)
    return created_user