"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django.contrib.auth.decorators import user_passes_test

def admin_required(view_func):
    """Ensure only users with the 'admin' role can access the view."""
    return user_passes_test(
        lambda u: u.is_authenticated and u.role == 'admin',
        login_url='/admin/login/'
    )(view_func)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include("account.urls")),
    path('',include("ride.urls")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path('api/docs/', admin_required(SpectacularSwaggerView.as_view(url_name='schema')), name='swagger-ui'),

    path('api/redoc/', admin_required(SpectacularRedocView.as_view(url_name='schema')), name='redoc'),
    
   
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)