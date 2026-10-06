from rest_framework import serializers
from .models import Favorite
from ..properties.serializers import ListPropertySerializer, Property


class ListFavoriteSerializer(serializers.ModelSerializer):
    property = ListPropertySerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["property", "created_at"]


class CreateFavoriteSerializer(serializers.ModelSerializer):
    property = serializers.PrimaryKeyRelatedField(
        queryset=Property.objects.all())

    class Meta:
        model = Favorite
        fields = ["property", "id"]
        read_only_fields = ["id"]
