import os
import unittest

import django
from django.conf import settings
from django.core.management import call_command

settings.configure(
    INSTALLED_APPS=["django.contrib.sessions"],
    DATABASES={"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}},
    DEFAULT_AUTO_FIELD="django.db.models.AutoField",
)
django.setup()

call_command("migrate")

current_dir = os.path.dirname(os.path.abspath(__file__))
unittest.TextTestRunner().run(unittest.defaultTestLoader.discover(current_dir))
