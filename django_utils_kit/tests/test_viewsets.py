from django_utils_kit.test_utils import APITestCase


class ImprovedViewSetTestCase(APITestCase):
    def test_list(self) -> None:
        # Should succeed because of custom permission
        response = self.api_client.get("/improved-viewset/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "BasicSerializer")

    def test_list_error(self) -> None:
        # get_valid_serializer should fail
        response = self.api_client.get("/improved-viewset/?error=true")
        self.assertEqual(response.status_code, 400)
        error = response.data["id"][0]
        self.assertEqual(error, "A valid integer is required.")

    def test_get(self) -> None:
        # Should fail because of default permission
        response = self.api_client.get("/improved-viewset/1/")
        self.assertEqual(response.status_code, 401)
