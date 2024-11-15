"""Additional serializers and fields for Django and DRF."""

from typing import Any, Dict

from django.conf import settings
from django.db.models import Model
from rest_framework import serializers

from django_utils_kit.images import image_to_base64


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    """`ModelSerializer` blocks create/update methods."""

    def create(self, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError

    def update(self, instance: Model, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError


class ThumbnailField(serializers.ImageField):
    """`ImageField` with a representation that returns a base64 downsized image."""

    def to_representation(self, data: serializers.ImageField) -> bytes:
        return image_to_base64(data, settings.MAX_THUMBNAIL_SIZE)
