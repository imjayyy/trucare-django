from django.urls import path

from .views import (
    IntakeAssignDoctorAPIView,
    IntakeClaimAPIView,
    IntakeDetailAPIView,
    IntakeDoctorListAPIView,
    IntakeFormAPIView,
    IntakeListView,
    IntakeSearchAPIView,
    IntakeStatusUpdateView,
    IntakeGetStatusView,
    IntakeConditionsView,
)


urlpatterns = [
    path("form/", IntakeFormAPIView.as_view(), name="intake-form"),
    path("list/", IntakeListView.as_view(), name="intake-list"),
    path("doctors/", IntakeDoctorListAPIView.as_view(), name="intake-doctors"),
    path("search/", IntakeSearchAPIView.as_view(), name="intake-search"),
    path("detail/", IntakeDetailAPIView.as_view(), name="intake-detail"),
    path("claim/", IntakeClaimAPIView.as_view(), name="intake-claim"),
    path("assign-doctor/", IntakeAssignDoctorAPIView.as_view(), name="intake-assign-doctor"),
    path("status-update/", IntakeStatusUpdateView.as_view(), name="intake-status-update"),
    path("get-status-by-role/", IntakeGetStatusView.as_view(), name="intake-get-status"),
    path("conditions/", IntakeConditionsView.as_view(), name="intake-conditions"),
]