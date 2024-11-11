from io import BytesIO
import os
import unittest

import django
from django.conf import settings
from django.core.files.storage import Storage
from django.core.management import call_command
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import path
from django.views import View
from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_kit.exceptions import Conflict, FailedPrecondition
from django_utils_kit.files import download_file, download_files_as_zip

# --------------------------------------------------
# Settings
# --------------------------------------------------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
settings.configure(
    # Security
    SECRET_KEY="secret",
    # Apps
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.contenttypes",
        "rest_framework",
    ],
    # Database
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    # DRF
    ROOT_URLCONF=__name__,
    REST_FRAMEWORK={
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.TokenAuthentication",
            "rest_framework.authentication.BasicAuthentication",
            "rest_framework.authentication.SessionAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
        "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
        "DEFAULT_PARSER_CLASSES": ("rest_framework.parsers.JSONParser",),
        "TEST_REQUEST_DEFAULT_FORMAT": "json",
    },
    # Emails
    TEMPLATES=[
        {
            "BACKEND": "django.template.backends.django.DjangoTemplates",
            "DIRS": [
                os.path.join(CURRENT_DIR, "templates"),
            ],
            "APP_DIRS": True,
        },
    ],
    DEFAULT_FROM_EMAIL="test@localhost.com",
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
)


# --------------------------------------------------
# Storage
# --------------------------------------------------
class MockStorage(Storage):
    def open(self, path: str, mode: str = "rb") -> BytesIO:
        content = f"Example file content {path}"
        return BytesIO(content.encode())

    def exists(self, name: str) -> bool:
        return True


# --------------------------------------------------
# Routes
# --------------------------------------------------
# Must be imported after settings.configure
from rest_framework.views import APIView  # noqa
from rest_framework.viewsets import GenericViewSet  # noqa
from django_utils_kit.permissions import BlockAll, IsNotAuthenticated  # noqa


class ConflictExampleView(APIView):
    def get(self, _request: Request) -> Response:
        raise Conflict()


class FailedPreconditionExampleView(APIView):
    def get(self, _request: Request) -> Response:
        raise FailedPrecondition()


class DownloadFileView(View):
    def get(self, request: Request) -> StreamingHttpResponse:
        return download_file("path/to/file.txt", MockStorage())


class DownloadZipFileView(View):
    def get(self, request: Request) -> HttpResponse:
        return download_files_as_zip(
            ["path/to/file1.txt", "path/to/file2.txt"], "output.zip", MockStorage()
        )


class BlockAllViewSet(GenericViewSet):
    permission_classes = [BlockAll]

    def list(self, request: Request) -> Response:
        return Response()


class IsNotAuthenticatedViewSet(GenericViewSet):
    permission_classes = [IsNotAuthenticated]

    def list(self, request: Request) -> Response:
        return Response(data={"is_authenticated": False})


urlpatterns = [
    path("conflict-example/", ConflictExampleView.as_view(), name="conflict-example"),
    path(
        "failed-precondition-example/",
        FailedPreconditionExampleView.as_view(),
        name="failed-precondition-example",
    ),
    path("download-file/", DownloadFileView.as_view(), name="download-file"),
    path("download-zip/", DownloadZipFileView.as_view(), name="download-file"),
    path("block-all/", BlockAllViewSet.as_view({"get": "list"}), name="block-all"),
    path(
        "is-not-authenticated/",
        IsNotAuthenticatedViewSet.as_view({"get": "list"}),
        name="is-not-authenticated",
    ),
]

# --------------------------------------------------
# Boot django
# --------------------------------------------------
django.setup()
call_command("migrate")

# --------------------------------------------------
# Trigger tests
# --------------------------------------------------
current_dir = os.path.dirname(os.path.abspath(__file__))
unittest.TextTestRunner().run(unittest.defaultTestLoader.discover(current_dir))
