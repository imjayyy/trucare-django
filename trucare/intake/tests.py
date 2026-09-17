from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from accounts.models import AccountProfile, DoctorProfile
from .models import Insurance, PatientInfo, PatientIntake

User = get_user_model()


class IntakeListViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="tester", email="tester@example.com", password="password")
        self.manager = User.objects.create_user(username="manager", email="manager@example.com", password="password")
        AccountProfile.objects.create(user=self.manager, role="MANAGER")
        self.agent = User.objects.create_user(username="agent", email="agent@example.com", password="password")
        self.doctor_user = User.objects.create_user(username="doctor", email="doctor@example.com", password="password")
        AccountProfile.objects.create(user=self.doctor_user, role="DOCTOR")
        self.doctor = DoctorProfile.objects.create(
            user=self.doctor_user,
            phone_number="5551234567",
            email="doctor@example.com",
            address="123 Main St",
            state="CA",
            npi="1234567890",
        )

        self.patient_one = PatientInfo.objects.create(
            first_name="Alice",
            last_name="Smith",
            date_of_birth="1990-01-01",
            email="alice@example.com",
            phone_number="5550000000",
            address="1 Test Street",
            state="CA",
        )
        self.intake_one = PatientIntake.objects.create(
            patient=self.patient_one,
            client=self.manager,
            intake_agent=self.agent,
            doctor=self.doctor,
            status="Pending",
        )
        Insurance.objects.create(
            patient=self.patient_one,
            insurance_type="RX",
            insurance_carrier="Acme RX",
            bin="123456",
            pcn="ABC",
            group_id="GROUP-1",
            patient_id_rx="PAT-001",
        )

        self.patient_two = PatientInfo.objects.create(
            first_name="Bob",
            last_name="Jones",
            date_of_birth="1985-05-05",
            email="bob@example.com",
            phone_number="5551111111",
            address="2 Test Avenue",
            state="TX",
        )
        self.intake_two = PatientIntake.objects.create(
            patient=self.patient_two,
            client=self.manager,
            intake_agent=self.agent,
            doctor=None,
            status="Completed",
        )
        Insurance.objects.create(
            patient=self.patient_two,
            insurance_type="RX",
            insurance_carrier="Acme RX",
            bin="999999",
            pcn="XYZ",
            group_id="GROUP-2",
            patient_id_rx="PAT-002",
        )

    def test_list_view_filters_and_paginates_results(self):
        client = APIClient()
        client.force_authenticate(self.user)

        response = client.get(
            reverse("intake-list"),
            {
                "first_name": "Ali",
                "insurance_bin": "123456",
                "patient_status": "Pending",
                "page_size": 1,
            },
        )

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["count"], 1)
        self.assertEqual(len(payload["results"]), 1)
        self.assertEqual(payload["results"][0]["first_name"], "Alice")
        self.assertEqual(payload["results"][0]["insurance_bin"], "123456")
        self.assertEqual(payload["results"][0]["status"], "Pending")

    def test_list_available_doctors(self):
        client = APIClient()
        client.force_authenticate(self.manager)

        response = client.get(reverse("intake-doctors"))

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertTrue(any(item["id"] == self.doctor.id for item in payload))

    def test_search_intake_by_id(self):
        client = APIClient()
        client.force_authenticate(self.manager)

        response = client.get(reverse("intake-search"), {"patient_id": self.patient_one.id})

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["patient_id"], self.patient_one.id)
        self.assertEqual(payload["status"], "Pending")

    def test_claim_intake(self):
        client = APIClient()
        client.force_authenticate(self.manager)

        response = client.post(
            reverse("intake-claim"),
            {"patient_id": self.patient_one.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.intake_one.refresh_from_db()
        self.assertEqual(self.intake_one.status, "Claimed")

    def test_assign_doctor_to_claimed_intake(self):
        self.intake_one.status = "Claimed"
        self.intake_one.save(update_fields=["status"])

        client = APIClient()
        client.force_authenticate(self.manager)

        response = client.post(
            reverse("intake-assign-doctor"),
            {"patient_id": self.patient_one.id, "doctor_id": self.doctor.id},
            format="json",
        )

        self.assertEqual(response.status_code, 200)
        self.intake_one.refresh_from_db()
        self.assertEqual(self.intake_one.doctor, self.doctor)
        self.assertEqual(self.intake_one.status, "Assigned")
