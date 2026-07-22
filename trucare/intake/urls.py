from django.urls import path

from .views import IntakeFormAPIView


urlpatterns = [
    path("form/", IntakeFormAPIView.as_view(), name="intake-form"),
]