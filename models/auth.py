from sqlalchemy import Column, Integer, String, Boolean

from db.db import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String(20), default="user")
    phone_number = Column(String(20), nullable=True)