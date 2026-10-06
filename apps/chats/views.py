from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from .serializers import CreateMessageSerializer, ListMessageSerializer, GetMessageSerializer
from .models import Message
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from ..properties.models import Property
from rest_framework.exceptions import PermissionDenied
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .permissions import IsAdminOrOwner

# Create your views here.


class CreateMessageView(CreateAPIView):
    serializer_class = CreateMessageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Message.objects.all()

    def perform_create(self, serializer):
        sender = self.request.user
        property = get_object_or_404(Property, pk=self.kwargs["pk"])
        if sender == property.seller:
            raise PermissionDenied({
                "detail": "Invalid request"
            })

        serializer.save(sender=sender, property=property)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(f"user_{property.seller.id}", {
            "type": "notification",
            "message": "You have a new notification"
        })


class ListMessagesView(ListAPIView):
    serializer_class = ListMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(property__seller=self.request.user)


class GetMessageView(RetrieveAPIView):
    serializer_class = GetMessageSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    queryset = Message.objects.all()
