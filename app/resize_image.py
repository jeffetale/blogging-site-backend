from PIL import Image
import io
import os
from fastapi import UploadFile
from typing import List, Tuple

async def process_and_save_image(file: UploadFile, filename: str) -> List[dict]:
    sizes = [(300, 200, "small"), (600, 400, "medium"), (1200, 800, "large")]

    output_path = os.path.join("static", "images")
    os.makedirs(output_path, exist_ok=True)

    content = await file.read()
    image = Image.open(io.BytesIO(content))

    processed_images = []

    for width, height, suffix in sizes:
        output_filename = (
            f"{os.path.splitext(filename)[0]}_{suffix}{os.path.splitext(filename)[1]}"
        )
        resized_image = image.copy()
        resized_image.thumbnail((width, height))

        # Create a new image with the target size and paste the resized image
        new_image = Image.new("RGB", (width, height), (255, 255, 255))
        paste_x = (width - resized_image.width) // 2
        paste_y = (height - resized_image.height) // 2
        new_image.paste(resized_image, (paste_x, paste_y))

        new_image.save(os.path.join(output_path, output_filename))

        processed_images.append(
            {
                "url": f"/static/images/{output_filename}",
                "width": width,
                "height": height,
            }
        )

    return processed_images
