# ✨ Django Utils Kit ✨

![Code quality](https://github.com/Jordan-Kowal/django-utils-kit/actions/workflows/code_quality.yml/badge.svg?branch=main)
![Tests](https://github.com/Jordan-Kowal/django-utils-kit/actions/workflows/tests.yml/badge.svg?branch=main)
![Build](https://github.com/Jordan-Kowal/django-utils-kit/actions/workflows/publish_package.yml/badge.svg?event=release)
![Coverage](https://badgen.net/badge/coverage/%3E90%25/pink)
![Tag](https://badgen.net/badge/tag/1.0.0/orange)
![Python](https://badgen.net/badge/python/3.9%20|%203.10%20|%203.11%20|%203.12|%203.13)
![Licence](https://badgen.net/badge/licence/MIT)

- [✨ Django Utils Kit ✨](#-django-utils-kit-)
  - [💻 How to install](#-how-to-install)
  - [📕 Available imports](#-available-imports)
  - [🔗 Useful links](#-useful-links)
  - [⏳ Stats](#-stats)

Provides various utilities for working with Django and DRF:

- [admin.py](./django_utils_kit/admin.py): Additional classes and mixins for Django admin.
- [emails.py](./django_utils_kit/emails.py): Classes to easily send sync and async emails through Django.
- [exceptions.py](./django_utils_kit/exceptions.py): Additional exceptions for DRF.
- [files.py](./django_utils_kit/files.py): Utilities for handling files with DRF.
- [images.py](./django_utils_kit/images.py): Utilities for handling images within Django.
- [models.py](./django_utils_kit/models.py): Additional classes and utilities for Django models.
- [network.py](./django_utils_kit/network.py): Network related utilities to handle requests.
- [permissions.py](./django_utils_kit/permissions.py): Additional permissions for DRF.
- [serializers.py](./django_utils_kit/serializers.py): Additional serializers and fields for DRF.
- [test_runner.py](./django_utils_kit/test_runner.py): Custom test runners for Django.
- [test_utils.py](./django_utils_kit/test_utils.py): Additional TestCase classes with new assertions and utilities.
- [viewsets.py](./django_utils_kit/viewsets.py): Custom ViewSets for DRF.

## 💻 How to install

The package is available on PyPi with the name `django-utils-kit`.
Simply run:

```shell
pip install django-utils-kit
```

## 📕 Available imports

Here's a list of all available imports for this package:

```python
from django_utils_kit.admin import ReadOnlyAdminMixin
from django_utils_kit.emails import Email
from django_utils_kit.exceptions import Conflict, FailedPrecondition
from django_utils_kit.files import download_file, download_files_as_zip
from django_utils_kit.images import (
    downsize_and_save_image_from_path,
    downsize_image,
    image_to_base64,
)
from django_utils_kit.models import (
    FileNameWithUUID,
    ImprovedModel,
    PreCleanedAbstractModel,
    update_m2m,
    update_model_instance,
)
from django_utils_kit.network import get_client_ip, get_server_domain
from django_utils_kit.permissions import BlockAll, IsNotAuthenticated
from django_utils_kit.serializers import ReadOnlyModelSerializer, ThumbnailField
from django_utils_kit.test_runners import TimedTestRunner
from django_utils_kit.test_utils import APITestCase, AssertionTestCase, ImprovedTestCase
from django_utils_kit.viewsets import ImprovedViewSet

```

## 🔗 Useful links

- [Want to contribute?](CONTRIBUTING.md)
- [See what's new!](CHANGELOG.md)

## ⏳ Stats

![Alt](https://repobeats.axiom.co/api/embed/7737e6de1232f7c80366bc34f2b2d78861727e2b.svg "Repobeats analytics image")
