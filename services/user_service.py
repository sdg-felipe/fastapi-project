from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from models.auth import UserModel

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(UserModel).filter(UserModel.username == username).first()

def create_user(db: Session, email: str, username: str, hashed_password: str, role: str, phone_number: str):
    try:
        new_user = UserModel(
            email=email,
            username=username,
            password=hashed_password,
            role=role,
            phone_number=phone_number
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Something went wrong")
