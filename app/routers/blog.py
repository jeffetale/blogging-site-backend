# app/routers/blog.py

from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Form
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/blog_posts", response_model=List[schemas.BlogPost])
def read_blog_posts(skip: int = 0, limit: int = 1000000, db: Session = Depends(get_db)):
    blog_posts = crud.get_blog_posts(db, skip=skip, limit=limit)
    return blog_posts


@router.get("/blog_posts/{post_id}", response_model=schemas.BlogPost)
def read_blog_post(post_id: int, db: Session = Depends(get_db)):
    blog_post = crud.get_blog_post(db, post_id=post_id)
    if blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post


@router.post("/blog_posts", response_model=schemas.BlogPost)
async def create_blog_post(
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    logger.info(f"Attempting to create blog post: title={title}, category={category}")
    try:
        blog_post = schemas.BlogPostCreate(
            title=title, content=content, category=category
        )
        created_post = await crud.create_blog_post(
            db=db, blog_post=blog_post, user_id=current_user.id, image=image
        )
        logger.info(f"Successfully created blog post with id: {created_post.id}")
        return created_post
    except Exception as e:
        logger.error(f"Error creating blog post: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/blog_posts/{post_id}/update_view_count", response_model=schemas.BlogPost)
def update_view_count(post_id: int, db: Session = Depends(get_db)):
    blog_post = crud.update_view_count(db, post_id)
    if blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post


@router.get("/popular_posts", response_model=List[schemas.BlogPost])
def read_popular_posts(db: Session = Depends(get_db)):
    popular_posts = crud.get_top_popular_posts(db)
    return popular_posts


@router.put("/blog_posts/{post_id}", response_model=schemas.BlogPost)
def update_blog_post(
    post_id: int,
    blog_post: schemas.BlogPostUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_blog_post = crud.update_blog_post(db, post_id, blog_post)
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog_post


@router.delete("/blog_posts/{post_id}", response_model=schemas.BlogPost)
def delete_blog_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    db_blog_post = crud.delete_blog_post(db, post_id)
    if db_blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return db_blog_post


@router.get("/blog_posts/{post_id}/is_owner")
def check_post_ownership(
    post_id: int,
    current_user: schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    is_owner = crud.is_post_owner(db, post_id, current_user.id)
    return {"is_owner": is_owner}
