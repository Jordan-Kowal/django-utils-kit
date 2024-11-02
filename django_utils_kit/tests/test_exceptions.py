from rest_framework.status import HTTP_409_CONFLICT

from django_utils_kit.test_utils import APITestCase


class ExceptionsTestCase(APITestCase):
    def test_conflict(self) -> None:
        response = self.api_client.get("/conflict-example/")
        self.assertEqual(response.status_code, HTTP_409_CONFLICT)
        self.assertEqual(
            response.data["detail"], "A similar object already exists in the database."
        )

    def test_failed_precondition(self) -> None:
        response = self.api_client.get("/failed-precondition-example/")
        self.assertEqual(response.status_code, 412)
        self.assertEqual(
            response.data["detail"], "One or several preconditions have not been met."
        )
