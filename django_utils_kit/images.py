"""Utilities for handling images within Django."""

import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Tuple

from django.core.files import File
from django.db.models import ImageField

# Third-party
from PIL import Image

IMAGE_TYPES = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def override_image_in_storage(img_field: ImageField, new_img: Image.Image) -> None:
    """Overrides an image in storage with a new image."""
    img_filename = Path(img_field.file.name).name
    img_ext = img_filename.split(".")[-1]
    img_format = IMAGE_TYPES[img_ext]
    buffer = BytesIO()
    new_img.save(buffer, format=img_format)
    file_object = File(buffer)
    img_field.save(img_filename, file_object)


def downsize_image(file_path: str, width: int, height: int) -> None:
    """Downsizes an image to the given dimensions while keeping its ratio."""
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def image_to_base64(data: str) -> bytes:
    """Converts an image to base64."""
    buffered = BytesIO()
    original_image = Image.open(data)
    original_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())


def maybe_resize_image(
    img: Image.Image, max_size: Optional[int] = None
) -> Tuple[bool, Image.Image]:
    """Resizes an image to the given max size while keeping its ratio."""
    min_length, max_length = sorted([img.width, img.height])
    resized = False
    if max_length > max_size:
        factor = round(max_size * min_length / max_length)
        dimensions = (
            (max_size, factor) if img.width == max_length else (factor, max_size)
        )
        img = img.resize(dimensions)
        resized = True
    return resized, img


def resized_image_to_base64(data: str, max_size: Optional[int] = None) -> bytes:
    """Resizes an image to the given max size and converts it to base64."""
    buffered = BytesIO()
    original_image = Image.open(data)
    _, resized_image = maybe_resize_image(original_image, max_size=max_size)
    resized_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())
