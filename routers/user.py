from fastapi import APIRouter, HTTPException
from dependencies.auth import user_dependency
from dependencies.db import db_dependency
from schemas.user import User
from services.user_service import get_user_by_id

router = APIRouter(
    prefix="/user",
    tags=["user"]
)

@router.get("/me", response_model=User)
async def read_current_user(db: db_dependency, current_user: user_dependency):
    user = get_user_by_id(db, current_user.get("id"))
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
