from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/blog_posts", response_model=List[schemas.BlogPost])
def read_blog_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    blog_posts = crud.get_blog_posts(db, skip=skip, limit=limit)
    return blog_posts

@router.get("/blog_posts/{post_id}", response_model=schemas.BlogPost)
def read_blog_post(post_id: int, db: Session = Depends(get_db)):
    blog_post = crud.get_blog_post(db, post_id=post_id)
    if blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post

@router.post("/blog_posts", response_model=schemas.BlogPost)
def create_blog_post(blog_post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    return crud.create_blog_post(db=db, blog_post=blog_post)


