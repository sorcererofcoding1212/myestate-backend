from django.urls import path
from . import views

app_name = "favorites"

urlpatterns = [
    path("", views.ListFavoritesView.as_view()),
    path("delete/<int:pk>/", views.DeleteFavoriteView.as_view())
]
