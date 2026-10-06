from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CreatePropertySerializer, GetPropertySerializer, ListPropertySerializer, SearchPropertySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Property
from rest_framework.response import Response
from rest_framework import status
from .models import PropertyImage
import json
from django.db.models import Case, When, Value, IntegerField
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from .filters import PropertyFilter

# Create your views here.


class CreatePropertyView(CreateAPIView):
    serializer_class = CreatePropertySerializer
    queryset = Property.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        property = serializer.save(seller=request.user)

        images = request.FILES.getlist("images")
        tags = request.data.getlist("tags")

        for image, tag in zip(images, tags):
            PropertyImage.objects.create(
                property=property, image=image, tag=tag)

        return Response({
            "detail": "Listing created"
        }, status=status.HTTP_201_CREATED)


class ListPropertyView(ListAPIView):
    serializer_class = ListPropertySerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Property.objects.filter(is_archived=False, approval_status=Property.ApprovalStatus.APPROVED,
                                           availability_status=Property.AvailabilityStatus.AVAILABLE).prefetch_related("images")

        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(seller=user)

        location = json.loads(self.request.query_params.get("location", "{}"))
        city = location.get("city")
        state = location.get("state")

        if not location:
            return queryset.order_by("-created_at")[:10]

        return (
            queryset
            .filter(state=state)
            .annotate(
                location_priority=Case(
                    When(city=city, then=Value(0)),
                    default=Value(1),
                    output_field=IntegerField(),
                )
            )
            .order_by("location_priority", "-created_at")[:10]
        )


class GetPropertyByIdView(RetrieveAPIView):
    serializer_class = GetPropertySerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        queryset = Property.objects.all()

        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(seller=user)

        return queryset


class QuickSearchPropertyView(ListAPIView):
    serializer_class = SearchPropertySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = Property.objects.filter(
            is_archived=False, approval_status=Property.ApprovalStatus.APPROVED, availability_status=Property.AvailabilityStatus.AVAILABLE)

        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(seller=user)

        q = self.request.query_params.get("q", "").strip()
        offset = int(self.request.query_params.get("offset"))

        if q:
            queryset = queryset.filter(
                Q(address__icontains=q) |
                Q(city__icontains=q) |
                Q(postal_code__icontains=q) |
                Q(state__icontains=q)
            )[:offset]

        return queryset


class AdvancedSearchPropertyView(ListAPIView):
    serializer_class = ListPropertySerializer
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PropertyFilter

    def get_queryset(self):
        queryset = Property.objects.filter(is_archived=False, availability_status=Property.AvailabilityStatus.AVAILABLE, approval_status=Property.ApprovalStatus.APPROVED)

        user = self.request.user
        if user.is_authenticated:
            queryset = queryset.exclude(seller=user)

        return queryset
