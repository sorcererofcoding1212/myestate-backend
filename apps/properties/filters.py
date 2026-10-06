import django_filters
from .models import Property


class CharInFilter(django_filters.BaseInFilter, django_filters.CharFilter):
    pass


class ChoiceInFilter(django_filters.BaseInFilter, django_filters.ChoiceFilter):
    pass


class PropertyFilter(django_filters.FilterSet):
    city = CharInFilter(lookup_expr="in", field_name="city")
    postal_code = django_filters.CharFilter()
    listing_type = django_filters.ChoiceFilter(
        choices=Property.ListingType.choices)
    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte")
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte")
    property_type = ChoiceInFilter(
        choices=Property.PropertyType.choices, field_name="property_type")
    bedrooms = django_filters.NumberFilter(lookup_expr="gte")
    min_area = django_filters.NumberFilter(
        field_name="area", lookup_expr="gte")
    max_area = django_filters.NumberFilter(
        field_name="area", lookup_expr="lte")
    furnishing_status = ChoiceInFilter(
        choices=Property.FurnishingStatus.choices, field_name="furnishing_status")

    class Meta:
        model = Property
        fields = ["city",
                  "postal_code",
                  "listing_type",
                  "property_type",
                  "bedrooms",
                  "furnishing_status"]
