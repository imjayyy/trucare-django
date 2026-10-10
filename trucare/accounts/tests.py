from django.contrib.auth import get_user_model
from datetime import date
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from intake.models import PatientInfo, PatientIntake
from .models import AccountProfile


User = get_user_model()


class RegisterAPIViewTests(APITestCase):
	def setUp(self):
		self.url = reverse("auth-register")
		self.payload = {
			"username": "new_manager",
			"email": "new.manager@example.com",
			"password": "StrongPassword123!",
			"role": AccountProfile.ROLE_MANAGER,
		}

	def test_register_requires_authentication(self):
		response = self.client.post(self.url, self.payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_register_forbidden_for_non_admin_user(self):
		manager_user = User.objects.create_user(
			username="manager_user",
			email="manager@example.com",
			password="StrongPassword123!",
		)
		AccountProfile.objects.create(user=manager_user, role=AccountProfile.ROLE_MANAGER)
		self.client.force_authenticate(user=manager_user)

		response = self.client.post(self.url, self.payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_register_allowed_for_admin_user(self):
		admin_user = User.objects.create_user(
			username="admin_user",
			email="admin@example.com",
			password="StrongPassword123!",
		)
		AccountProfile.objects.create(user=admin_user, role=AccountProfile.ROLE_ADMIN)
		self.client.force_authenticate(user=admin_user)

		response = self.client.post(self.url, self.payload, format="json")

		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
		self.assertEqual(response.data["username"], self.payload["username"])
		self.assertTrue(User.objects.filter(username=self.payload["username"]).exists())


class PasswordChangeViewTests(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(
			username="password_user",
			email="password@example.com",
			password="OldPassword123!",
		)
		self.client.force_authenticate(user=self.user)
		self.url = reverse("auth-change-password")

	def test_change_password_successfully(self):
		response = self.client.patch(
			self.url,
			{"old_password": "OldPassword123!", "new_password": "NewPassword456!"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password("NewPassword456!"))

	def test_change_password_rejects_wrong_old_password(self):
		response = self.client.patch(
			self.url,
			{"old_password": "WrongPassword123!", "new_password": "NewPassword456!"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password("OldPassword123!"))

	def test_change_password_requires_authentication(self):
		self.client.force_authenticate(user=None)

		response = self.client.patch(
			self.url,
			{"old_password": "OldPassword123!", "new_password": "NewPassword456!"},
			format="json",
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class DashboardAPIViewTests(APITestCase):
	def setUp(self):
		self.admin = User.objects.create_user(username="dashboard_admin", password="password")
		AccountProfile.objects.create(user=self.admin, role=AccountProfile.ROLE_ADMIN)
		self.agency = User.objects.create_user(username="dashboard_agency", password="password")
		AccountProfile.objects.create(
			user=self.agency,
			role=AccountProfile.ROLE_ORGANIZATION,
			organization_type=AccountProfile.ORG_AGENCY,
		)
		self.other_agency = User.objects.create_user(username="other_agency", password="password")
		AccountProfile.objects.create(
			user=self.other_agency,
			role=AccountProfile.ROLE_ORGANIZATION,
			organization_type=AccountProfile.ORG_AGENCY,
		)
		self.url = reverse("auth-dashboard")

	def create_intake(self, client, email, intake_status):
		patient = PatientInfo.objects.create(
			first_name="Test",
			last_name="Patient",
			date_of_birth=date(1990, 1, 1),
			email=email,
		)
		return PatientIntake.objects.create(patient=patient, client=client, status=intake_status)

	def test_admin_dashboard_counts_requested_system_metrics(self):
		self.create_intake(self.agency, "assigned@example.com", "ASSIGNED_TO_DOCTOR")
		self.create_intake(self.agency, "approved@example.com", "APPROVED_BY_DOCTOR")
		self.create_intake(self.agency, "provider-decline@example.com", "PROVIDER_DECLINE")
		self.create_intake(self.agency, "patient-decline@example.com", "PATIENT_DECLINE")
		self.client.force_authenticate(self.admin)

		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["dashboard_type"], "system")
		self.assertEqual(response.data["patients_added_this_month"], 4)
		self.assertEqual(response.data["patients_assigned_to_doctor"], 1)
		self.assertEqual(response.data["doctor_approvals_this_week"], 1)
		self.assertEqual(response.data["doctor_approvals_this_month"], 1)
		self.assertEqual(response.data["provider_declines_this_month"], 1)
		self.assertEqual(response.data["patient_declines_this_month"], 1)

	def test_agency_dashboard_only_counts_its_own_intakes(self):
		self.create_intake(self.agency, "agency-approved@example.com", "APPROVED_BY_DOCTOR")
		self.create_intake(self.other_agency, "other-agency-approved@example.com", "APPROVED_BY_DOCTOR")
		self.client.force_authenticate(self.agency)

		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data["dashboard_type"], "agency")
		self.assertEqual(response.data["intake_submissions_this_week"], 1)
		self.assertEqual(response.data["intake_submissions_this_month"], 1)
		self.assertEqual(response.data["doctor_approvals_this_week"], 1)
		self.assertEqual(response.data["doctor_approvals_this_month"], 1)

	def test_unsupported_role_cannot_view_dashboard(self):
		user = User.objects.create_user(username="dashboard_doctor", password="password")
		AccountProfile.objects.create(user=user, role=AccountProfile.ROLE_DOCTOR)
		self.client.force_authenticate(user)

		response = self.client.get(self.url)

		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
