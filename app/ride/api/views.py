from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.db.models import F, OuterRef, Subquery
from django.db.models.functions import Sqrt, Power
from drf_spectacular.utils import extend_schema
from account.permissons import IsAdminUserRole
from rest_framework.permissions import IsAuthenticated

from ride.models import *
from .serializers import RideSerializer

class RidePagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 100

class RideListAPIView(ListAPIView):
    queryset = Ride.objects.select_related('rider', 'driver').prefetch_related('events')
    serializer_class = RideSerializer
    pagination_class = RidePagination
    permission_classes = [IsAuthenticated,IsAdminUserRole]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'rider__email']
    ordering_fields = ['pickup_time', 'distance']


    @extend_schema(
        summary="User Login",
        description="Authenticate user and return JWT tokens",
        tags=["Authentication"]
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        # Handle GPS-based distance sorting
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')
        if latitude and longitude:
            latitude = float(latitude)
            longitude = float(longitude)
            queryset = queryset.annotate(
                distance=Sqrt(
                    Power(F('pickup_latitude') - latitude, 2) +
                    Power(F('pickup_longitude') - longitude, 2)
                )
            )

        return queryset
