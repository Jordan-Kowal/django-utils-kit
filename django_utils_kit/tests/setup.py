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
settings.configure(
    INSTALLED_APPS=[
        "django.contrib.admin",
        "django.contrib.auth",
        "django.contrib.sessions",
        "django.contrib.contenttypes",
        "rest_framework",
    ],
    SECRET_KEY="secret",
    ROOT_URLCONF=__name__,
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
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


urlpatterns = [
    path("conflict-example/", ConflictExampleView.as_view(), name="conflict-example"),
    path(
        "failed-precondition-example/",
        FailedPreconditionExampleView.as_view(),
        name="failed-precondition-example",
    ),
    path("download-file/", DownloadFileView.as_view(), name="download-file"),
    path("download-zip/", DownloadZipFileView.as_view(), name="download-file"),
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
