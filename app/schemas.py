from pydantic import BaseModel, EmailStr
from typing import Optional
from . import models
from datetime import datetime

# Contact
class ContactBase(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    image: Optional[str] = None
    reminder: Optional[int] = None

class UpdateContact(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None 
    image: Optional[str] = None
    reminder: Optional[int] = None

class ContactResponse(BaseModel):
    id: int
    first_name: str
    last_name: Optional[str] = None
    days_since_last_hangout: int
    phone_number: Optional[str] = None
    image: Optional[str] = None
    reminder: Optional[int] = None
    created_at: datetime
    

# USERS
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str


# TOKENS
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
