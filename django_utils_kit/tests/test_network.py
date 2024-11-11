from django.test import RequestFactory, override_settings

from django_utils_kit.network import get_client_ip, get_server_domain
from django_utils_kit.test_utils import ImprovedTestCase


class NetworkTestCase(ImprovedTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.factory = RequestFactory()

    def test_get_client_ip(self) -> None:
        request = self.factory.get("/my-url/")
        # Only REMOTE_ADDR is set
        request.META["REMOTE_ADDR"] = "127.0.0.1"
        self.assertEqual(get_client_ip(request), "127.0.0.1")
        # If HTTP_X_REAL_IP is set, it takes precedence
        request.META["HTTP_X_REAL_IP"] = "127.0.0.2"
        self.assertEqual(get_client_ip(request), "127.0.0.2")
        # If HTTP_X_FORWARDED_FOR is set, it takes precedence
        request.META["HTTP_X_FORWARDED_FOR"] = "127.0.0.3"
        self.assertEqual(get_client_ip(request), "127.0.0.3")

    @override_settings(ALLOWED_HOSTS=["expected.com", "ignored.com"])
    def test_get_server_domain_with_hosts(self) -> None:
        self.assertEqual(get_server_domain(), "expected.com")
        self.assertEqual(get_server_domain("default.com"), "expected.com")

    @override_settings(ALLOWED_HOSTS=[])
    def test_get_server_domain_without_hosts(self) -> None:
        self.assertEqual(get_server_domain(), "http://127.0.0.1:8000/")
        self.assertEqual(get_server_domain("default.com"), "default.com")
