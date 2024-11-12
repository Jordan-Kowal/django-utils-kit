from django.test import override_settings

from django_utils_kit.images import image_to_base64
from django_utils_kit.serializers import ReadOnlyModelSerializer, ThumbnailField
from django_utils_kit.test_utils import ImprovedTestCase
from django_utils_kit.tests.fixtures import GITHUB_LOGO_PATH


class ReadOnlyModelSerializerTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        self.serializer = ReadOnlyModelSerializer()

    def test_create(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.serializer.create({})

    def test_update(self) -> None:
        with self.assertRaises(NotImplementedError):
            self.serializer.update({}, {})


class ThumbnailFieldTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        self.field = ThumbnailField()

    def test_to_representation(self) -> None:
        image = self.uploaded_file_from_path(GITHUB_LOGO_PATH)
        base64 = image_to_base64(image)
        repr = self.field.to_representation(image)
        self.assertNotEqual(base64, repr)

    @override_settings(MAX_THUMBNAIL_SIZE=1000)
    def test_to_representation_max_size(self) -> None:
        image = self.uploaded_file_from_path(GITHUB_LOGO_PATH)
        base64 = image_to_base64(image)
        repr = self.field.to_representation(image)
        self.assertEqual(base64, repr)
