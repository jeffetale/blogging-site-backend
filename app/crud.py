# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users(db: Session, skip: int = 0, limit: int = 1000000):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_blog_posts(db: Session, skip: int = 0, limit: int = 1000000):
    return db.query(models.BlogPost).offset(skip).limit(limit).all()

def get_blog_post(db: Session, post_id: int):
    return db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()

def create_blog_post(db: Session, blog_post: schemas.BlogPostCreate):
    db_blog_post = models.BlogPost(**blog_post.model_dump())
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

def create_contact_message(db: Session, contact_message: schemas.ContactMessageCreate):
    db_contact_message = models.ContactMessage(**contact_message.model_dump())
    db.add(db_contact_message)
    db.commit()
    db.refresh(db_contact_message)
    return db_contact_message

def update_view_count(db: Session, post_id: int):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if blog_post:
        blog_post.view_count += 1
        db.commit()
        db.refresh(blog_post)
    return blog_post

def get_top_popular_posts(db: Session, limit: int = 3):
    return db.query(models.BlogPost).order_by(models.BlogPost.view_count.desc()).limit(limit).all()
