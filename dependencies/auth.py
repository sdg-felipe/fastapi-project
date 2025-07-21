from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from fastapi import HTTPException
from core.config import JWT_SECRET, JWT_ALGORITHM

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        username: str = payload.get("username")
        user_id: str = payload.get("id")
        if username is None and user_id is None:
            raise HTTPException(status_code=401, detail="Could not get user")
        return {
            "username": username,
            "id": user_id
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not get user")

user_dependency = Annotated[dict, Depends(get_current_user)]