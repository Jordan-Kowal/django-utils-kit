from django.contrib.auth.models import User
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN

from django_utils_kit.test_utils import APITestCase


class BlockAllTestCase(APITestCase):
    def test_block_all(self) -> None:
        response = self.api_client.get("/block-all/")
        self.assertEqual(response.status_code, HTTP_401_UNAUTHORIZED)


class IsNotAuthenticatedTestCase(APITestCase):
    def setUp(self) -> None:
        super().setUp()
        self.api_client.logout()

    def test_when_not_authenticated(self) -> None:
        response = self.api_client.get("/is-not-authenticated/")
        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data["is_authenticated"], False)

    def test_when_authenticated(self) -> None:
        user = User.objects.create_user(username="testuser", password="testpassword")
        self.api_client.force_authenticate(user=user)
        response = self.api_client.get("/is-not-authenticated/")
        self.assertEqual(response.status_code, HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.data["detail"], "You must be logged out to use this service"
        )
