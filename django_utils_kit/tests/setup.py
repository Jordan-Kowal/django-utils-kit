import os
import unittest

import django
from django.conf import settings
from django.core.management import call_command
from django.urls import path
from rest_framework.request import Request
from rest_framework.response import Response

from django_utils_kit.exceptions import Conflict, FailedPrecondition

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


urlpatterns = [
    path("conflict-example/", ConflictExampleView.as_view(), name="conflict-example"),
    path(
        "failed-precondition-example/",
        FailedPreconditionExampleView.as_view(),
        name="failed-precondition-example",
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
