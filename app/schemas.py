# app/schemas.py

from pydantic import BaseModel, EmailStr
from typing import Optional

class BlogPostBase(BaseModel):
    title: str
    content: str
    category: str
    image_url: str
    view_count: int = 0

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None

class BlogPost(BlogPostBase):
    id: int
    class Config:
        orm_mode = True

class ContactMessageBase(BaseModel):
    name: str
    email: EmailStr
    message: str

class ContactMessageCreate(ContactMessageBase):
    pass

class ContactMessage(ContactMessageBase):
    id: int
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

