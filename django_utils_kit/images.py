"""Utilities for handling images within Django."""

import base64
from io import BytesIO
from typing import Optional, Tuple

from PIL import Image

IMAGE_TYPES = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "gif": "GIF",
    "tif": "TIFF",
    "tiff": "TIFF",
}


def downsize_and_save_image_from_path(file_path: str, width: int, height: int) -> None:
    """
    Given a image file path, downsizes it to the given dimensions while keeping its ratio.
    Does nothing if the image is already small-enough.

    Args:
        file_path (str): path to the existing image
        width (int): width to downsize to
        height (int): height to downsize to
    """
    img = Image.open(file_path)
    if (img.height > height) or (img.width > width):
        output_size = (width, height)
        img.thumbnail(output_size)
        img.save(file_path)


def downsize_image(img: Image.Image, max_size: int) -> Tuple[bool, Image.Image]:
    """
    Resizes an image to the given max size while keeping its ratio.
    Does not save the resized image, returns it instead.

    Args:
        img (Image.Image): Image object to resize
        max_size (int): max size to resize to

    Returns:
        Tuple[bool, Image.Image]: resized, image
    """
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


def image_to_base64(file_path: str, downsize_to: Optional[int] = None) -> bytes:
    """
    Converts an image to base64, optionally downsizing it.

    Args:
        file_path (str): path to the existing image
        downsize_to (Optional[int]): max size to resize to

    Returns:
        bytes: base64 representation of the image
    """
    buffered = BytesIO()
    image = Image.open(file_path)
    format = image.format
    if downsize_to:
        _, image = downsize_image(image, downsize_to)
    image.save(buffered, format=format)
    return base64.b64encode(buffered.getvalue())
