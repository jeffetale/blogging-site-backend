# app/models.py

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from slugify import slugify

Base = declarative_base()


class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    summary = Column(Text)
    short_summary = Column(Text)
    category = Column(String, index=True)
    image_url_small = Column(String)
    image_url_medium = Column(String)
    image_url_large = Column(String)
    image_public_id_small = Column(String)
    image_public_id_medium = Column(String)
    image_public_id_large = Column(String)
    view_count = Column(Integer, nullable=True, default=0)
    slug = Column(String, unique=True, index=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="blog_posts")

    def generate_slug(self, db):
        base_slug = slugify(self.title)
        slug = base_slug
        counter = 1

        while True:
            existing_post = db.query(BlogPost).filter_by(slug=slug).first()
            if not existing_post or existing_post.id == self.id:
                break
            slug = f"{base_slug}-{counter}"
            counter += 1

        return slug


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    blog_posts = relationship("BlogPost", back_populates="user")

class ContactMessage(Base):
    __tablename__ = 'contact_messages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, index=True)
    message = Column(Text)
    created_at =Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
