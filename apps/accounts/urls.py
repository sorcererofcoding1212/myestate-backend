from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

app_name = "accounts"

urlpatterns = [
    path("register/", views.RegisterAccountView.as_view()),
    path("verify-otp/", views.VerifyOTPView.as_view()),
    path("login/", views.LoginAccountView.as_view()),
    path("logout/", views.LogoutAccountView.as_view()),
    path("me/", views.ValidateSessionView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
    path("password-reset/link/", views.GenerateResetPasswordLinkView.as_view()),
    path("password-reset/", views.ResetPasswordView.as_view()),
]
