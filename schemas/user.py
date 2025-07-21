from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    email: str
    phone_number: str = ""
    role: str = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str
    email: str
