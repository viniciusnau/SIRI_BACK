from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "id",
            "user",
            "name",
            "stock",
            "email",
        )


class ClientNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ("id", "name")
