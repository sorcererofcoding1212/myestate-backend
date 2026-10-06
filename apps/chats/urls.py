from django.urls import path
from . import views

app_name = "chats"

urlpatterns = [
    path("", views.ListMessagesView.as_view()),
    path("<int:pk>/create/", views.CreateMessageView.as_view()),
    path("<int:pk>/", views.GetMessageView.as_view())
]
