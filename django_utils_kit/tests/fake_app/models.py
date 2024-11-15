from django.db import models

from django_utils_kit.models import (
    FileNameWithUUID,
    ImprovedModel,
    PreCleanedAbstractModel,
)


class ImprovedUser(PreCleanedAbstractModel, ImprovedModel):
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255)
    avatar = models.ImageField(
        upload_to=FileNameWithUUID("django_utils_kit/tests/fake_app/avatars"),
        null=True,
        blank=True,
    )
    tags = models.ManyToManyField("Tag")

    class Meta:
        abstract = False

    def _pre_save(self) -> None:
        print("Pre save")

    def _post_save(self) -> None:
        print("Post save")

    def _pre_delete(self) -> None:
        print("Pre delete")

    def _post_delete(self) -> None:
        print("Post delete")


class Tag(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(ImprovedUser)
