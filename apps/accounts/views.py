from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import AccountSerializer, TokenObtainPairAndUserObjectSerializer, PasswordResetSerializer, GeneratePasswordResetLinkSerializer
from .models import Account
from django.core.cache import cache
import secrets
from services.mail_service import send_verification_email, send_password_reset_link
from rest_framework.views import APIView
from .serializers import OTPVerificationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from smtplib import SMTPException
from django.conf import settings

# Create your views here.


class RegisterAccountView(CreateAPIView):
    serializer_class = AccountSerializer
    permission_classes = [AllowAny]
    queryset = Account.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        otp = secrets.randbelow(900000) + 100000

        cached_data = serializer.validated_data.copy()
        cached_data["otp"] = str(otp)
        email = cached_data["email"]

        cache.set(f"registration:{email}", cached_data, timeout=60*30)

        try:
            send_verification_email(email, otp)
        except SMTPException:
            cache.delete(f"registration:{email}")
            return Response({
                "detail": "Unable to send verification email."
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        return Response({
            "detail": "OTP sent to your email"
        }, status=status.HTTP_201_CREATED)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = OTPVerificationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        cached_data = cache.get(f"registration:{email}")
        if not cached_data:
            return Response({
                "detail": "OTP is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        if cached_data["otp"] != str(otp):
            return Response({
                "detail": "OTP is invalid or expired"
            }, status=status.HTTP_400_BAD_REQUEST)

        cached_data.pop("otp")

        cached_password = cached_data.pop("password")

        user = Account.objects.create_user(
            password=cached_password, **cached_data)

        cache.delete(f"registration:{email}")

        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Account registered",
            "user": AccountSerializer(user).data,
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)


class LoginAccountView(TokenObtainPairView):
    serializer_class = TokenObtainPairAndUserObjectSerializer


class LogoutAccountView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        refresh = request.data.get("refresh")

        token = RefreshToken(refresh)
        token.blacklist()

        return Response({
            "detail": "Logged out"
        }, status=status.HTTP_200_OK)


class ValidateSessionView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, *args, **kwargs):
        user = request.user
        serialized_user = AccountSerializer(user).data

        return Response({
            "detail": "Session validated",
            "user": serialized_user
        }, status=status.HTTP_200_OK)


class GenerateResetPasswordLinkView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = GeneratePasswordResetLinkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = Account.objects.filter(email=email).first()

        if not user:
            return Response({
                "detail": "User does not exist"
            }, status=status.HTTP_400_BAD_REQUEST)

        token = secrets.token_urlsafe(32)

        cache.set(f"password_reset:{token}", {"email": email}, timeout=60*15)

        password_reset_link = f"{settings.FRONTEND_URL}/password/reset?t={token}"

        send_password_reset_link(email, password_reset_link)

        return Response({
            "detail": "Password reset link sent to your registered email address"
        }, status=status.HTTP_200_OK)


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.query_params.get("t")

        cached_data = cache.get(f"password_reset:{token}")
        if not cached_data:
            return Response({
                "detail": "Token expired or invalid"
            }, status=status.HTTP_400_BAD_REQUEST)

        cached_email = cached_data.pop("email")

        user = Account.objects.get(email=cached_email)

        serializer = PasswordResetSerializer(
            data=request.data, context={"user": user})
        
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["password"]

        user.set_password(new_password)

        user.save()

        cache.delete(f"password_reset:{token}")

        return Response({
            "detail": "Password updated"
        }, status=status.HTTP_200_OK)
