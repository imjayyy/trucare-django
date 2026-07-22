from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

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
