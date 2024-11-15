import os
import shutil
import unittest

import django
from django.conf import settings
from django.core.management import call_command
from django.urls import path

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
        "django_utils_kit.tests.fake_app.apps.FakeAppConfig",
    ],
    # Database
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
    # Images
    MAX_THUMBNAIL_SIZE=100,
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
# Routes
# --------------------------------------------------
from django_utils_kit.tests.fake_app import views  # noqa

urlpatterns = [
    path(
        "conflict-example/",
        views.ConflictExampleView.as_view(),
        name="conflict-example",
    ),
    path(
        "failed-precondition-example/",
        views.FailedPreconditionExampleView.as_view(),
        name="failed-precondition-example",
    ),
    path("download-file/", views.DownloadFileView.as_view(), name="download-file"),
    path("download-zip/", views.DownloadZipFileView.as_view(), name="download-file"),
    path(
        "block-all/", views.BlockAllViewSet.as_view({"get": "list"}), name="block-all"
    ),
    path(
        "is-not-authenticated/",
        views.IsNotAuthenticatedViewSet.as_view({"get": "list"}),
        name="is-not-authenticated",
    ),
    path(
        "improved-viewset/",
        views.ImprovedViewSetExample.as_view({"get": "list"}),
        name="improved-viewset",
    ),
    path(
        "improved-viewset/<int:pk>/",
        views.ImprovedViewSetExample.as_view({"get": "retrieve"}),
        name="improved-viewset",
    ),
]

# --------------------------------------------------
# Boot django
# --------------------------------------------------
django.setup()
call_command("makemigrations", "fake_app")
call_command("migrate")

# --------------------------------------------------
# Trigger tests
# --------------------------------------------------
# Run tests
current_dir = os.path.dirname(os.path.abspath(__file__))
test_runner = unittest.TextTestRunner()
results = test_runner.run(unittest.defaultTestLoader.discover(current_dir))

# Remove migrations
migration_dir = os.path.join(current_dir, "fake_app", "migrations")
if os.path.exists(migration_dir):
    shutil.rmtree(migration_dir)

# Remove images
avatars_dir = os.path.join(current_dir, "fake_app", "avatars")
if os.path.exists(avatars_dir):
    shutil.rmtree(avatars_dir)

# Raise if tests failed
if results.errors or results.failures:
    raise Exception("Tests failed. See errors above.")
