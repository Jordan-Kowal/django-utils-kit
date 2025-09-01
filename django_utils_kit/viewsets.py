"""Custom ViewSets for DRF."""

from collections.abc import Sequence
from typing import Any

from rest_framework.permissions import BasePermission
from rest_framework.serializers import BaseSerializer
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet


class ImprovedViewSet(GenericViewSet):
    """
    Allows permissions and serializers to be defined per action,
    and provides various utilities for working with viewsets.
    """

    default_permission_classes: Sequence[type[BasePermission]] = ()
    default_serializer_class: type[BaseSerializer] | None = None
    permission_classes_per_action: dict[str, Sequence[type[BasePermission]]] = {}
    serializer_class_per_action: dict[str, type[BaseSerializer]] = {}

    def get_permissions(self) -> list[BasePermission]:
        permissions = self.permission_classes_per_action.get(
            self.action, self.default_permission_classes
        )
        if len(permissions) == 0:
            permissions = api_settings.DEFAULT_PERMISSION_CLASSES
        return [permission() for permission in permissions]

    def get_serializer_class(self) -> type[BaseSerializer] | None:
        return self.serializer_class_per_action.get(
            self.action, self.default_serializer_class
        )

    def get_valid_serializer(self, *args: Any, **kwargs: Any) -> BaseSerializer:
        serializer = self.get_serializer(*args, **kwargs)
        serializer.is_valid(raise_exception=True)
        return serializer
