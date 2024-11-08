"""Additional serializers and fields for Django and DRF."""

from typing import Any, Dict

from django.conf import settings
from django.db.models import Model
from rest_framework import serializers

from django_utils_kit.images import resized_image_to_base64


class ReadOnlyModelSerializer(serializers.ModelSerializer):
    """A `ModelSerializer` that only allows for reading."""

    def create(self, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError

    def update(self, instance: Model, validated_data: Dict[str, Any]) -> Model:
        raise NotImplementedError


class ThumbnailField(serializers.ImageField):
    """A `serializers.ImageField` that returns a thumbnail."""

    def to_representation(self, data: serializers.ImageField) -> bytes:
        return resized_image_to_base64(data, settings.MAX_THUMBNAIL_SIZE)
