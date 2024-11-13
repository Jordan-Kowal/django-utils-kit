"""Utilities for handling images within Django."""

import base64
from io import BytesIO
from typing import Tuple

from PIL import Image

IMAGE_TYPES = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def downsize_image(file_path: str, width: int, height: int) -> None:
    """Downsizes an image to the given dimensions while keeping its ratio."""
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def image_to_base64(file_path: str) -> bytes:
    """Converts an image to base64."""
    buffered = BytesIO()
    original_image = Image.open(file_path)
    original_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())


def maybe_downsize_image(img: Image.Image, max_size: int) -> Tuple[bool, Image.Image]:
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


def downsize_image_to_base64(data: str, max_size: int) -> bytes:
    """Resizes an image to the given max size and converts it to base64."""
    buffered = BytesIO()
    original_image = Image.open(data)
    _, resized_image = maybe_downsize_image(original_image, max_size)
    resized_image.save(buffered, format=original_image.format)
    return base64.b64encode(buffered.getvalue())
