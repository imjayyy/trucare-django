
from .views import (DoctorDeniedAPIView, PrescriptionAPIView, PrescriptionDataAPIView, 
                    PrescriptionPDFAPIView, GenerateSoapNotesAPIView, BillerPDFAPIView, 
                    DoctorDeniedAPIView)

from .views import GenerateSoapNotesAPIView

from django.urls import path

urlpatterns = [
    path("save/<int:intake_id>/", PrescriptionAPIView.as_view(), name="prescription-api"),
    path("doctor-denied/", DoctorDeniedAPIView.as_view(), name="doctor-denied-api"),
    path("data/", PrescriptionDataAPIView.as_view(), name="prescription-data-api"),
    path("pdf/", PrescriptionPDFAPIView.as_view(), name="prescription-pdf-api"),
    path("<int:intake_id>/soap-notes/", GenerateSoapNotesAPIView.as_view(), name="generate-soap-notes"),
    path("biller-pdf/", BillerPDFAPIView.as_view(), name="biller-pdf-api"),
    path("soap-notes/", GenerateSoapNotesAPIView.as_view(), name="save-soap-notes"),
        ]