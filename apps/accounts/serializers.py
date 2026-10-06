from rest_framework import serializers
from .models import Account
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "email", "first_name", "last_name", "password"]
        read_only_fields = ["id"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        return Account.objects.create_user(**validated_data)


class AccountInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name", "email"]


class OTPVerificationSerializer(serializers.Serializer):
    otp = serializers.IntegerField()
    email = serializers.EmailField()


class GeneratePasswordResetLinkSerializer(serializers.Serializer):
    email = serializers.EmailField()


class TokenObtainPairAndUserObjectSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = AccountSerializer(self.user).data
        return data


class PasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

    def validate_password(self, value):
        user = self.context["user"]

        if user.check_password(value):
            raise serializers.ValidationError(
                "Your new password must be different from your current password")

        return value
