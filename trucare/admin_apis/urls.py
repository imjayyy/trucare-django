from django.urls import path

from .finance_views import (
    ClientFinanceDetailAPIView,
    ClientFinanceListCreateAPIView,
    DoctorFinanceDetailAPIView,
    DoctorFinanceListCreateAPIView,
)
from .registration_views import (
    DoctorDetailAPIView,
    DoctorListCreateAPIView,
    BillingDetailAPIView,
    BillingListCreateAPIView,
    ManagerDetailAPIView,
    ManagerListCreateAPIView,
    OrganizationDetailAPIView,
    OrganizationListCreateAPIView,
)
from .pharmacy_views import (
    PharmacyListCreateAPIView,
    PharmacyDetailAPIView,
)


urlpatterns = [
    path("managers/", ManagerListCreateAPIView.as_view(), name="admin-manager-list-create"),
    path("managers/<int:manager_id>/", ManagerDetailAPIView.as_view(), name="admin-manager-detail"),
    path("billers/", BillingListCreateAPIView.as_view(), name="admin-biller-list-create"),
    path("billers/<int:biller_id>/", BillingDetailAPIView.as_view(), name="admin-biller-detail"),
    path("finances/doctors/", DoctorFinanceListCreateAPIView.as_view(), name="admin-doctor-finance-list-create"),
    path("finances/doctors/<int:finance_id>/", DoctorFinanceDetailAPIView.as_view(), name="admin-doctor-finance-detail"),
    path("finances/clients/", ClientFinanceListCreateAPIView.as_view(), name="admin-client-finance-list-create"),
    path("finances/clients/<int:finance_id>/", ClientFinanceDetailAPIView.as_view(), name="admin-client-finance-detail"),
    path("organizations/", OrganizationListCreateAPIView.as_view(), name="admin-organization-list-create"),
    path("organizations/<int:organization_id>/", OrganizationDetailAPIView.as_view(), name="admin-organization-detail"),
    path("doctors/", DoctorListCreateAPIView.as_view(), name="admin-doctor-list-create"),
    path("doctors/<int:doctor_id>/", DoctorDetailAPIView.as_view(), name="admin-doctor-detail"),
    path("pharmacies/", PharmacyListCreateAPIView.as_view(), name="admin-pharmacy-list-create"),
    path("pharmacies/<int:pharmacy_id>/", PharmacyDetailAPIView.as_view(), name="admin-pharmacy-detail"),
]
