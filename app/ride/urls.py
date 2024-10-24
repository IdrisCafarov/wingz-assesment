from django.urls import path
from ride.api.views import RideListAPIView

urlpatterns = [
    path('rides/', RideListAPIView.as_view(), name='ride-list'),
]
