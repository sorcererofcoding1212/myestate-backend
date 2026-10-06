from django.urls import path
from . import views

app_name = "properties"

urlpatterns = [
    path("", views.ListPropertyView.as_view()),
    path("<int:pk>/", views.GetPropertyByIdView.as_view()),
    path("create/", views.CreatePropertyView.as_view()),
    path("quick-search/", views.QuickSearchPropertyView.as_view()),
    path("advanced-search/", views.AdvancedSearchPropertyView.as_view())
]
