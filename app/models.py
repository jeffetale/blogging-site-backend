# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BlogPost(Base):
    __tablename__ = 'blog_posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    category = Column(String, index=True)
    image_url = Column(String)
    view_count = Column(Integer, nullable=True, default=0)


class ContactMessage(Base):
    __tablename__ = 'contact_messages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    message = Column(Text)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at =Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())