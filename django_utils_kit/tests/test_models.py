from unittest.mock import call, patch

from django import forms
from django.db import IntegrityError

from django_utils_kit.models import update_m2m, update_model_instance
from django_utils_kit.test_utils import ImprovedTestCase
from django_utils_kit.tests.fake_app.models import ImprovedUser, Tag
from django_utils_kit.tests.fixtures import GITHUB_LOGO_PATH


class ModelsTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.print_mocker = patch("builtins.print")
        self.full_clean_mocker = patch(
            "django_utils_kit.tests.fake_app.models.ImprovedUser.full_clean"
        )
        self.print_mock = self.print_mocker.start()
        self.full_clean_mock = self.full_clean_mocker.start()

    def tearDown(self) -> None:
        self.print_mocker.stop()
        self.full_clean_mocker.stop()
        super().tearDown()

    def test_save_workflow(self) -> None:
        user = ImprovedUser(first_name="John", last_name="Doe")
        user.save()
        self.assertEqual(
            self.print_mock.call_args_list, [call("Pre save"), call("Post save")]
        )
        user.delete()
        self.assertEqual(
            self.print_mock.call_args_list,
            [
                call("Pre save"),
                call("Post save"),
                call("Pre delete"),
                call("Post delete"),
            ],
        )

    def test_auto_clean(self) -> None:
        # Should call full_clean
        user = ImprovedUser(first_name="John", last_name="Doe")
        user.save()
        self.assertEqual(self.full_clean_mock.call_count, 1)
        # Form errors are converted to IntegrityErrors
        self.full_clean_mock.side_effect = forms.ValidationError("Invalid")
        with self.assertRaises(IntegrityError):
            user = ImprovedUser(first_name="", last_name="Doe")
            user.save()
        # Other errors stay the same
        self.full_clean_mock.side_effect = RuntimeError("Invalid")
        with self.assertRaises(RuntimeError):
            user = ImprovedUser(first_name="", last_name="Doe")
            user.save()

    def test_file_name_with_uuid(self) -> None:
        image = self.uploaded_file_from_path(GITHUB_LOGO_PATH)
        user = ImprovedUser(first_name="John", last_name="Doe", avatar=image)
        user.save()
        pattern = r"avatars/github-logo_[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}.png"
        self.assertRegex(user.avatar.name, pattern)

    def test_update_model_instance(self) -> None:
        user = ImprovedUser(first_name="John", last_name="Doe")
        user.save()
        updated_user = update_model_instance(user, first_name="John2", last_name="Doe2")
        instance = ImprovedUser.objects.get(id=user.id)
        self.assertEqual(updated_user.first_name, "John2")
        self.assertEqual(updated_user.last_name, "Doe2")
        self.assertEqual(instance.first_name, "John2")
        self.assertEqual(instance.last_name, "Doe2")

    def test_update_m2m(self) -> None:
        tag_1 = Tag.objects.create(name="Tag 1")
        tag_2 = Tag.objects.create(name="Tag 2")
        tag_3 = Tag.objects.create(name="Tag 3")
        user = ImprovedUser.objects.create(first_name="John", last_name="Doe")
        user.tags.add(tag_1, tag_2)
        update_m2m(user.tags, [tag_2.id, tag_3.id])
        instance = ImprovedUser.objects.get(id=user.id)
        self.assertEqual(list(instance.tags.all()), [tag_2, tag_3])
