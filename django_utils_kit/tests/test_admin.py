from django_utils_kit.admin import ReadOnlyAdminMixin
from django_utils_kit.test_utils import ImprovedTestCase


class AdminTestCase(ImprovedTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.admin = ReadOnlyAdminMixin()

    def test_has_add_permission(self) -> None:
        request = self.build_fake_request()
        self.assertFalse(self.admin.has_add_permission(request))

    def test_has_delete_permission(self) -> None:
        request = self.build_fake_request()
        self.assertFalse(self.admin.has_delete_permission(request))

    def test_has_change_permission(self) -> None:
        request = self.build_fake_request()
        self.assertFalse(self.admin.has_change_permission(request))
