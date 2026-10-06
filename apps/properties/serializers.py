from rest_framework import serializers
from .models import Property
from ..accounts.serializers import AccountInformationSerializer
from ..favorites.models import Favorite


class CreatePropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ["description", "address", "city", "state", "postal_code", "bedrooms", "bathrooms", "area", "total_floors",
                  "floor_number", "balconies", "parking_spaces", "property_type", "listing_type", "price", "latitude", "longitude"]


class ListPropertySerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ["id", "address", "city", "state", "postal_code", "area",
                  "price", "property_type", "listing_type", "bathrooms", "bedrooms", "img"]

    def get_img(self, obj):
        img = obj.images.filter(tag="cover").first()

        if not img:
            return {"image": "https://static.vecteezy.com/system/resources/thumbnails/067/013/953/small/luxury-house-with-modern-landscape-free-photo.jpg", "tag": "cover"}

        request = self.context["request"]

        return {"image": request.build_absolute_uri(img.image.url), "tag": img.tag}


class GetPropertySerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()
    seller = AccountInformationSerializer(read_only=True)
    favorite_id = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ["id", "address", "city", "state", "postal_code", "area",
                  "price", "property_type", "listing_type", "bathrooms", "bedrooms", "banner", "images", "latitude", "longitude", "balconies", "parking_spaces", "total_floors", "floor_number", "description", "seller", "furnishing_status", "favorite_id"]

    def get_banner(self, obj):
        img = obj.images.filter(tag="cover").first()

        if not img:
            return {"image": "https://static.vecteezy.com/system/resources/thumbnails/067/013/953/small/luxury-house-with-modern-landscape-free-photo.jpg", "tag": "cover"}

        request = self.context["request"]

        return {"image": request.build_absolute_uri(img.image.url), "tag": img.tag}

    def get_images(self, obj):
        request = self.context["request"]

        images = []

        for img in obj.images.all():
            image_url = request.build_absolute_uri(img.image.url)
            tag = img.tag
            images.append({"image": image_url, "tag": tag})

        return images

    def get_favorite_id(self, obj):
        user = self.context["request"].user

        if not user.is_authenticated:
            return None
        
        favorite = Favorite.objects.filter(user=user, property=obj).first()

        if not favorite:
            return None

        return favorite.id


class SearchPropertySerializer(serializers.ModelSerializer):
    banner = serializers.SerializerMethodField()

    class Meta:
        model = Property
        fields = ["address", "city", "state", "postal_code",
                  "banner", "listing_type", "property_type", "id"]

    def get_banner(self, obj):
        img = obj.images.filter(tag="cover").first()

        if not img:
            return {"image": "https://static.vecteezy.com/system/resources/thumbnails/067/013/953/small/luxury-house-with-modern-landscape-free-photo.jpg", "tag": "cover"}

        request = self.context["request"]

        return request.build_absolute_uri(img.image.url)
