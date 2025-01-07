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
    summary: Optional[str] = None


class SuccessResponse(BaseModel):
    detail: str

class BlogPostInDB(BlogPostBase):
    id: int
    slug: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    user_id: int
    image_url_small: str
    image_url_medium: str
    image_url_large: str
    image_public_id_small: Optional[str] = None
    image_public_id_medium: Optional[str] = None
    image_public_id_large: Optional[str] = None
    summary: str

    class Config:
        from_attributes = True


class BlogPost(BlogPostBase):
    id: int
    slug: str
    image_url_small: str
    image_url_medium: str
    image_url_large: str
    image_public_id_small: Optional[str] = None
    image_public_id_medium: Optional[str] = None
    image_public_id_large: Optional[str] = None
    user_id: int
    summary: str
    short_summary: str

    class Config:
        from_attributes = True


class BlogPostSummary(BaseModel):
    id: int
    title: str
    summary: str
    short_summary: str
    category: str
    image_url_small: str
    image_url_medium: str
    image_url_large: str
    image_public_id_small: Optional[str] = None 
    image_public_id_medium: Optional[str] = None 
    image_public_id_large: Optional[str] = None 
    slug: str

    class Config:
        from_attributes = True


class PopularBlogPost(BaseModel):
    id: int
    title: str
    summary: str
    category: str
    image_url_medium: str
    image_public_id_medium: Optional[str] = None
    view_count: int
    slug: str

    class Config:
        from_attributes = True


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
        from_attributes = True

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
        from_attributes = True
