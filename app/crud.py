from sqlalchemy.orm import Session
from . import models, schemas

def get_blog_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.BlogPost).offset(skip).limit(limit).all()

def get_blog_post(db: Session, post_id: int):
    return db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()

def create_blog_post(db: Session, blog_post: schemas.BlogPostCreate):
    db_blog_post = models.BlogPost(**blog_post.dict())
    db.add(db_blog_post)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post

def create_contact_message(db: Session, contact_message: schemas.ContactMessageCreate):
    db_contact_message = models.ContactMessage(**contact_message.dict())
    db.add(db_contact_message)
    db.commit()
    db.refresh(db_contact_message)
    return db_contact_message