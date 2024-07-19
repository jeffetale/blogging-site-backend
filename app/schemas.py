# app/schemas.py

from pydantic import BaseModel, EmailStr

class BlogPostBase(BaseModel):
    title: str
    content: str
    category: str
    image_url: str
    view_count: int = 0

class BlogPostCreate(BlogPostBase):
    pass

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