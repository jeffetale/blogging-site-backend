# app/utils/cloudinary_helper.py

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
import io
from typing import List
from dotenv import load_dotenv
import os

load_dotenv()

CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

cloudinary.config(
    cloud_name=CLOUD_NAME.strip(),
    api_key=API_KEY.strip(),
    api_secret=API_SECRET.strip(),
)

try:
    from PIL import Image
except ImportError:
    # Fallback for environments where PIL isn't available
    Image = None
    print("WARNING: PIL not available, image processing will be limited")

async def upload_image(file: UploadFile, filename: str) -> List[dict]:
    try:
        # Get the raw content
        content = await file.read()

        # Direct upload to Cloudinary without PIL processing
        processed_images = []
        sizes = [
            {"width": 300, "height": 200, "suffix": "small"},
            {"width": 600, "height": 400, "suffix": "medium"},
            {"width": 1200, "height": 800, "suffix": "large"},
        ]

        for size in sizes:
            transformation = {
                "width": size["width"],
                "height": size["height"],
                "crop": "fill",
                "quality": "auto",
            }

            try:
                upload_result = cloudinary.uploader.upload(
                    content,
                    public_id=f"{filename}_{size['suffix']}",
                    transformation=transformation,
                )

                processed_images.append({
                    "url": upload_result["secure_url"],
                    "width": size["width"],
                    "height": size["height"],
                })
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error uploading image to Cloudinary: {str(e)}"
                )

        return processed_images
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


def delete_image(public_id: str) -> bool:
    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get("result") == "ok"
    except Exception as e:
        print(f"Error deleting image from Cloudinary: {str(e)}")
        return False
