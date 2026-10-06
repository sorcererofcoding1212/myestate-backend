from django.db import models
from django.contrib.auth import get_user_model
from ..properties.models import Property

# Create your models here.

Account = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name="outbox")
    property = models.ForeignKey(
        to=Property, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=10)
    date = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)

    class MessageType(models.TextChoices):
        VIEWING_REQUEST = "VIEWING_REQUEST", "Viewing Request"
        CONTACT_MESSAGE = "CONTACT_MESSAGE", "Contact Message"

    message_type = models.CharField(max_length=20, choices=MessageType.choices)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["sender", "property"], name="unique_sender_property")
        ]
