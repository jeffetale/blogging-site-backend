# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class BlogPostBase(BaseModel):
    title: str
    content: str
    category: str
    view_count: int = 0


class BlogPostCreate(BlogPostBase):
    pass 


class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None


class BlogPostInDB(BlogPostBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    image_url_small: str
    image_url_medium: str
    image_url_large: str

    class Config:
        orm_mode = True


class BlogPost(BlogPostInDB):
    pass


class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessage(ContactMessageBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
