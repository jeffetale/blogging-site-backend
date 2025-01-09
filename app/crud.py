# app/crud.py

from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext
from fastapi import UploadFile, HTTPException
from .utils.cloudinary_helper import upload_image, delete_image
import logging
from .llm import summarize_content
from .overview_llm import short_summarized_content
from datetime import datetime

logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username, email=user.email, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

async def upload_profile_image(db: Session, image: UploadFile):
    try:
        filename = f"profile_image_{datetime.now().timestamp()}"
        processed_image = await upload_image(image, filename)

        # Create new profile image record
        db_image = models.ProfileImage(
            image_url=processed_image[1]["url"],  # Using medium size
            image_public_id=f"{filename}_medium",
        )

        db.add(db_image)
        db.commit()
        db.refresh(db_image)

        return db_image
    except Exception as e:
        logger.error(f"Error in upload_profile_image: {str(e)}")
        raise


async def set_active_profile_image(db: Session, image_id: int):
    try:
        # Set all images to inactive
        db.query(models.ProfileImage).update({"is_active": False})

        # Set selected image to active
        image = (
            db.query(models.ProfileImage)
            .filter(models.ProfileImage.id == image_id)
            .first()
        )
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        image.is_active = True
        db.commit()

        return image
    except Exception as e:
        logger.error(f"Error in set_active_profile_image: {str(e)}")
        raise


async def delete_profile_image(db: Session, image_id: int):
    try:
        image = (
            db.query(models.ProfileImage)
            .filter(models.ProfileImage.id == image_id)
            .first()
        )
        if not image:
            raise HTTPException(status_code=404, detail="Image not found")

        delete_image(image.image_public_id)

        db.delete(image)
        db.commit()
        return {"message": "Image deleted successfully"}
    except Exception as e:
        logger.error(f"Error in delete_profile_image: {str(e)}")
        raise


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


async def create_blog_post(
    db: Session, blog_post: schemas.BlogPostCreate, user_id: int, image: UploadFile
):
    try:
        logger.info(f"Processing image for blog post: {blog_post.title}")
        filename = f"{blog_post.title.replace(' ', '_')}_{user_id}"
        processed_images = await upload_image(image, filename)

        # Create blog post without summaries first
        db_blog_post = models.BlogPost(
            **blog_post.model_dump(),
            user_id=user_id,
            image_url_small=processed_images[0]["url"],
            image_url_medium=processed_images[1]["url"],
            image_url_large=processed_images[2]["url"],
            image_public_id_small=f"{filename}_small",
            image_public_id_medium=f"{filename}_medium",
            image_public_id_large=f"{filename}_large",
        )

        # Generate slug before saving
        db_blog_post.slug = db_blog_post.generate_slug(db)

        # Add blog post to the database
        db.add(db_blog_post)
        db.commit()
        db.refresh(db_blog_post)

        # Return the post ID for background processing
        return db_blog_post

    except Exception as e:
        logger.error(f"Error in create_blog_post: {str(e)}")
        raise


async def generate_summaries(db: Session, post_id: int):
    try:
        blog_post = get_blog_post(db, post_id)
        if not blog_post:
            raise ValueError(f"Blog post {post_id} not found")

        # Generate summaries
        summary = summarize_content(blog_post.content)
        short_summary = short_summarized_content(blog_post.content)

        # Update the blog post with summaries
        blog_post.summary = summary
        blog_post.short_summary = short_summary
        db.commit()

    except Exception as e:
        logger.error(f"Error generating summaries for post {post_id}: {str(e)}")
        raise


def get_blog_post_by_slug(db: Session, slug: str):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.slug == slug).first()
    if not blog_post:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post


def update_blog_post(db: Session, post_id: int, blog_post: schemas.BlogPostUpdate):
    db_blog_post = (
        db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    )
    if not db_blog_post:
        return None
    for key, value in blog_post.model_dump(exclude_unset=True).items():
        setattr(db_blog_post, key, value)
    db.commit()
    db.refresh(db_blog_post)
    return db_blog_post


def create_contact_message(db: Session, contact_message: schemas.ContactMessageCreate):
    db_contact_message = models.ContactMessage(**contact_message.model_dump())
    db.add(db_contact_message)
    db.commit()
    db.refresh(db_contact_message)
    return db_contact_message


def get_contact_message(db: Session, message_id: int):
    contact_message = db.query(models.ContactMessage).filter(models.ContactMessage.id == message_id).first()
    if not contact_message:
        raise HTTPException(status_code=404, detail="Contact message not found")
    return contact_message


def get_all_contact_messages(db: Session, skip: int = 0, limit: int = 1000):
    return db.query(models.ContactMessage).offset(skip).limit(limit).all()


def update_view_count(db: Session, post_id: int):
    blog_post = db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    if blog_post:
        blog_post.view_count += 1
        db.commit()
        db.refresh(blog_post)
    return blog_post


def get_top_popular_posts(db: Session, limit: int = 3):
    return (
        db.query(models.BlogPost)
        .order_by(models.BlogPost.view_count.desc())
        .limit(limit)
        .all()
    )


def delete_blog_post(db: Session, post_id: int):
    db_blog_post = (
        db.query(models.BlogPost).filter(models.BlogPost.id == post_id).first()
    )
    if db_blog_post:
        # Delete images from Cloudinary
        for public_id in [
            db_blog_post.image_public_id_small,
            db_blog_post.image_public_id_medium,
            db_blog_post.image_public_id_large,
        ]:
            delete_image(public_id)

        db.delete(db_blog_post)
        db.commit()
        return schemas.SuccessResponse(detail="Blog post deleted successfully")
    return schemas.SuccessResponse(detail="Blog post not found")


def is_post_owner(db: Session, post_id: int, user_id: int):
    post = (
        db.query(models.BlogPost)
        .filter(models.BlogPost.id == post_id, models.BlogPost.user_id == user_id)
        .first()
    )
    return post is not None
