"""Additional classes and mixins for Django admin."""

from typing import Optional

from django.db.models import Model
from django.http.request import HttpRequest


class ReadOnlyAdminMixin:
    """Removes all write permissions for the admin view."""

    @staticmethod
    def has_add_permission(request: HttpRequest, obj: Optional[Model] = None) -> bool:
        return False

    @staticmethod
    def has_delete_permission(
        request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        return False

    @staticmethod
    def has_change_permission(
        request: HttpRequest, obj: Optional[Model] = None
    ) -> bool:
        return False
