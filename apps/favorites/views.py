from rest_framework.generics import ListCreateAPIView, DestroyAPIView
from .serializers import ListFavoriteSerializer, CreateFavoriteSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Favorite

# Create your views here.


class ListFavoritesView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateFavoriteSerializer

        return ListFavoriteSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeleteFavoriteView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
