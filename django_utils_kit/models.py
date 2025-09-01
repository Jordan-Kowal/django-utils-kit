"""Additional classes and utilities for Django models."""

import os
from typing import Any
import uuid

from django import forms
from django.db import IntegrityError, models
from django.utils.deconstruct import deconstructible


class ImprovedModel(models.Model):
    """
    Improved version of the Django Model class, with various utilities:
    - Add pre_save and post_save hooks
    - Add pre_delete and post_delete hooks
    """

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._pre_save()
        super().save(*args, **kwargs)
        self._post_save()

    def delete(self, *args: Any, **kwargs: Any) -> None:
        self._pre_delete()
        super().delete(*args, **kwargs)
        self._post_delete()

    def _pre_save(self) -> None:
        pass

    def _post_save(self) -> None:
        pass

    def _pre_delete(self) -> None:
        pass

    def _post_delete(self) -> None:
        pass


class PreCleanedAbstractModel(models.Model):
    """Model that calls .full_clean() before saving."""

    class Meta:
        abstract = True

    def save(self, *args: Any, **kwargs: Any) -> None:
        self._perform_pre_save_clean()
        super().save(*args, **kwargs)

    def _perform_pre_save_clean(self) -> None:
        """Calls .full_clean() and changes ValidationErrors to IntegrityErrors."""
        try:
            self.full_clean()
        except forms.ValidationError as e:
            raise IntegrityError(e)
        except Exception as e:
            raise e


@deconstructible
class FileNameWithUUID(object):
    """
    Will add a random UUID to the filename before saving it.

    Usage:
        >>> models.ImageField(
        ...     upload_to=FileNameWithUUID("django_utils_kit/tests/fake_app/avatars"),
        ...     null=True,
        ...     blank=True,
        ... )
    """

    def __init__(self, path: str) -> None:
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _: Any, filename: str) -> str:
        name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        return self.path % (name + "_" + str(uuid.uuid4()), extension)


def update_model_instance(instance: models.Model, **kwargs: Any) -> models.Model:
    """
    Shortcut to update a model instance with the provided fields/values (kwargs).

    Args:
        instance (models.Model): The model instance to update.
        **kwargs: The fields/values to update.

    Returns:
        models.Model: The updated model instance.
    """
    for key, value in kwargs.items():
        setattr(instance, key, value)
    instance.save()
    return instance


def update_m2m(
    m2m_field: models.Manager,
    ids: list[str],
) -> None:
    """
    Overrides the given m2m field with the provided ids

    Args:
        m2m_field (models.Manager): The m2m field to update
        ids (list[str]): The ids to set on the m2m field

    Usage:
        >>> update_m2m(instance.tags, [tag_1.id, tag_2.id])
    """
    unique_ids = set(ids or [])
    existing_m2m_fks = m2m_field.all().values_list("id", flat=True)
    # Delete m2m instances that are not in the provided ids
    m2m_fks_to_delete = [id_ for id_ in existing_m2m_fks if id_ not in unique_ids]
    if len(m2m_fks_to_delete) > 0:
        m2m_field.remove(*m2m_fks_to_delete)
    # Create m2m instances that are not in the existing instances
    fks_to_add = [id_ for id_ in unique_ids if id_ not in existing_m2m_fks]
    if len(fks_to_add) > 0:
        m2m_field.add(*fks_to_add)
