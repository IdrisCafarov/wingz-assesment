from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.views import RiderRegistrationViewSet, DriverRegistrationViewSet, LoginView



router = DefaultRouter()
router.register(r'rider', RiderRegistrationViewSet, basename='rider-registration')
router.register(r'driver', DriverRegistrationViewSet, basename='driver-registration')



urlpatterns = [
    path('login/', LoginView.as_view(), name='login'), 
    path('', include(router.urls)), 
]
