# app/routers/profile.py

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from .. import crud, models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter()


@router.post("/profile/images", response_model=schemas.ProfileImage)
async def upload_profile_image(
    image: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")

    # Add size validation if needed
    file_size = 0
    file_contents = await image.read()
    await image.seek(0)  # Reset file position
    if len(file_contents) > 5 * 1024 * 1024:  # 5MB limit
        raise HTTPException(status_code=400, detail="File too large")

    return await crud.upload_profile_image(db=db, image=image)


@router.put(
    "/profile/images/{image_id}/set-active", response_model=schemas.ProfileImage
)
async def set_active_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return await crud.set_active_profile_image(db=db, image_id=image_id)


@router.get("/profile/images", response_model=List[schemas.ProfileImage])
async def get_profile_images(
    db: Session = Depends(get_db),
):
    return db.query(models.ProfileImage).all()


@router.get("/profile/images/active", response_model=schemas.ProfileImage)
async def get_active_profile_image(
    db: Session = Depends(get_db),
):
    image = (
        db.query(models.ProfileImage)
        .filter(models.ProfileImage.is_active == True)
        .first()
    )
    if not image:
        raise HTTPException(status_code=404, detail="No active profile image found")
    return image


@router.delete("/profile/images/{image_id}")
async def delete_profile_image(
    image_id: int,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_user),
):
    return await crud.delete_profile_image(db=db, image_id=image_id)
