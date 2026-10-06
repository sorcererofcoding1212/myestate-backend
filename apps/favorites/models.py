from django.db import models
from ..properties.models import Property
from django.contrib.auth import get_user_model

Account = get_user_model()

# Create your models here.


class Favorite(models.Model):
    property = models.ForeignKey(
        to=Property, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["property", "user"], name="unique_property_user_favorite")]