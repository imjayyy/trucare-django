"""
URL configuration for trucare project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from accounts.views import DashboardAPIView
from django.views.static import serve
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/auth/', include('accounts.urls')),
    path('api/admin/', include('admin_apis.urls')),
    path('api/intake/', include('intake.urls')),
    path('api/scriptbuilder/', include('scriptbuilder.urls')),
    path('api/prescription/', include('prescription.urls')),
    path("api/dashboard/", DashboardAPIView.as_view(), name="auth-dashboard"),

]

urlpatterns += [
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
]
urlpatterns += [
    path(
        'doctor_signatures/<path:path>',
        serve,
        {'document_root': settings.BASE_DIR},
    ),
]
