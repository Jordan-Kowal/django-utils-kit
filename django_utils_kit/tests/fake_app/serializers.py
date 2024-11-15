from rest_framework import serializers


class BasicSerializer(serializers.Serializer):
    id = serializers.IntegerField()
