from django.db import models
from django.contrib.auth import get_user_model

Account = get_user_model()

# Create your models here.


class Property(models.Model):
    description = models.TextField(max_length=3000)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=6)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    area = models.DecimalField(max_digits=10, decimal_places=2)
    total_floors = models.PositiveIntegerField(blank=True, null=True)
    floor_number = models.PositiveIntegerField(blank=True, null=True)
    balconies = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_archived = models.BooleanField(default=False)
    parking_spaces = models.PositiveSmallIntegerField(default=0)
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
    )

    seller = models.ForeignKey(
        to=Account, on_delete=models.CASCADE, related_name="properties")

    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        SOLD = "SOLD", "Sold"
        RENTED = "RENTED", "Rented"

    availability_status = models.CharField(
        max_length=10, choices=AvailabilityStatus.choices, default=AvailabilityStatus.AVAILABLE)

    class ApprovalStatus(models.TextChoices):
        APPROVED = "APPROVED", "Approved"
        PENDING = "PENDING", "Pending"
        REJECTED = "REJECTED", "Rejected"

    approval_status = models.CharField(
        max_length=10, choices=ApprovalStatus.choices, default=ApprovalStatus.PENDING)

    class FurnishingStatus(models.TextChoices):
        FURNISHED = "FURNISHED", "Furnished"
        SEMI_FURNISHED = "SEMI_FURNISHED", "Semi Furnished"
        UNFURNISHED = "UNFURNISHED", "Unfurnished"

    furnishing_status = models.CharField(
        max_length=50, choices=FurnishingStatus.choices)

    class PropertyType(models.TextChoices):
        HOUSE = "HOUSE", "House"
        VILLA = "VILLA", "Villa"
        APARTMENT = "APARTMENT", "Apartment"

    property_type = models.CharField(
        max_length=10, choices=PropertyType.choices)

    class ListingType(models.TextChoices):
        SALE = "SALE", "Sale"
        RENT = "RENT", "Rent"
        
    listing_type = models.CharField(max_length=10, choices=ListingType.choices)

    def __str__(self):
        return self.address


class PropertyImage(models.Model):
    property = models.ForeignKey(
        to=Property, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="uploads/property/")
    tag = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
