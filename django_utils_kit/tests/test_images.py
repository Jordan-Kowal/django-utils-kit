import os

from PIL import Image

from django_utils_kit.images import (
    downsize_image,
    downsize_image_to_base64,
    image_to_base64,
    maybe_downsize_image,
)
from django_utils_kit.test_utils import ImprovedTestCase
from django_utils_kit.tests.fixtures import FIXTURES_DIR, GITHUB_LOGO_PATH

IMAGE_COPY_PATH = os.path.join(FIXTURES_DIR, "github-logo-copy.png")


class ImagesTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        super().setUp()
        img = Image.open(GITHUB_LOGO_PATH)
        img.save(IMAGE_COPY_PATH)

    def tearDown(self) -> None:
        super().tearDown()
        if os.path.exists(IMAGE_COPY_PATH):
            os.remove(IMAGE_COPY_PATH)

    def test_downsize_image(self) -> None:
        # Original image
        with open(IMAGE_COPY_PATH, "rb") as f:
            original_content = f.read()
        # Downsize to 100x100
        downsize_image(IMAGE_COPY_PATH, 100, 100)
        with open(IMAGE_COPY_PATH, "rb") as f:
            downsize_content = f.read()
        self.assertNotEqual(original_content, downsize_content)
        # Re-downsize to 200x200, which should do nothing
        downsize_image(IMAGE_COPY_PATH, 200, 200)
        with open(IMAGE_COPY_PATH, "rb") as f:
            unchanged_content = f.read()
        self.assertEqual(downsize_content, unchanged_content)

    def test_image_to_base64(self) -> None:
        result = image_to_base64(IMAGE_COPY_PATH)
        self.assertIs(type(result), bytes)

    def test_maybe_downsize_image(self) -> None:
        image = Image.open(IMAGE_COPY_PATH)
        # No resize needed
        resized, unchanged_image = maybe_downsize_image(image, 1000)
        self.assertFalse(resized)
        self.assertEqual(image.width, 512)
        self.assertEqual(image.height, 512)
        self.assertEqual(image.height, unchanged_image.height)
        self.assertEqual(image.width, unchanged_image.width)
        # Resize to 100
        resized, resized_image = maybe_downsize_image(image, 100)
        self.assertTrue(resized)
        self.assertEqual(image.width, 512)
        self.assertEqual(image.height, 512)
        self.assertEqual(resized_image.height, 100)
        self.assertEqual(resized_image.width, 100)

    def test_downsize_image_to_base64(self) -> None:
        original_value = image_to_base64(IMAGE_COPY_PATH)
        unchanged_value = downsize_image_to_base64(IMAGE_COPY_PATH, 600)
        changed_value = downsize_image_to_base64(IMAGE_COPY_PATH, 100)
        self.assertEqual(original_value, unchanged_value)
        self.assertNotEqual(original_value, changed_value)
        self.assertIs(type(original_value), bytes)
        self.assertIs(type(unchanged_value), bytes)
        self.assertIs(type(changed_value), bytes)
