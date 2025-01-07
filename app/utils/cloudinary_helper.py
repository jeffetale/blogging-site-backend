# app/utils/cloudinary_helper.py

import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
import io
from typing import List
from PIL import Image
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Get environment variables
CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
API_KEY = os.getenv("CLOUDINARY_API_KEY")
API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

# Validate environment variables
if not all([CLOUD_NAME, API_KEY, API_SECRET]):
    raise ValueError(
        "Missing Cloudinary credentials. Please check your .env file contains: "
        "CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, and CLOUDINARY_API_SECRET"
    )

# Configure Cloudinary
cloudinary.config(
    cloud_name=CLOUD_NAME.strip(),
    api_key=API_KEY.strip(),
    api_secret=API_SECRET.strip(),
)


async def upload_image(file: UploadFile, filename: str) -> List[dict]:
    try:
        sizes = [
            {"width": 300, "height": 200, "suffix": "small"},
            {"width": 600, "height": 400, "suffix": "medium"},
            {"width": 1200, "height": 800, "suffix": "large"},
        ]

        # Handle both file-like objects and raw content
        if hasattr(file, "read") and callable(file.read):
            content = await file.read()
        else:
            content = file.file  # Use the content directly if already read

        image = Image.open(io.BytesIO(content))

        processed_images = []

        for size in sizes:
            # Create transformation options for Cloudinary
            transformation = {
                "width": size["width"],
                "height": size["height"],
                "crop": "fill",
                "quality": "auto",
            }

            # Upload to Cloudinary with the specific transformation
            try:
                upload_result = cloudinary.uploader.upload(
                    content,
                    public_id=f"{filename}_{size['suffix']}",
                    transformation=transformation,
                )

                processed_images.append(
                    {
                        "url": upload_result["secure_url"],
                        "width": size["width"],
                        "height": size["height"],
                    }
                )
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error uploading image to Cloudinary: {str(e)}",
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
