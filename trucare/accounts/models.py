from django.db import models
from django.contrib.auth import get_user_model
from intake.models import states


User = get_user_model()


class AccountProfile(models.Model):
	ROLE_ADMIN = "ADMIN"
	ROLE_MANAGER = "MANAGER"
	ROLE_ORGANIZATION = "ORGANIZATION"
	ROLE_INTAKE_AGENT = "INTAKE_AGENT"
	ROLE_BILLING = "BILLING"
	ROLE_DOCTOR = "DOCTOR"

	ROLE_CHOICES = [
		(ROLE_ADMIN, "Admin"),
		(ROLE_MANAGER, "Manager"),
		(ROLE_ORGANIZATION, "Organization"),
		(ROLE_INTAKE_AGENT, "Intake Agent"),
		(ROLE_BILLING, "Billing"),
		(ROLE_DOCTOR, "Doctor"),
	]

	ORG_AGENCY = "AGENCY"
	ORG_CLIENT = "CLIENT"
	ORGANIZATION_TYPE_CHOICES = [
		(ORG_AGENCY, "Agency"),
		(ORG_CLIENT, "Client"),
	]

	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="account_profile",
	)
	role = models.CharField(max_length=20, choices=ROLE_CHOICES)
	organization_type = models.CharField(
		max_length=10,
		choices=ORGANIZATION_TYPE_CHOICES,
		blank=True,
		null=True,
	)
	parent_organization = models.ForeignKey(
		User,
		on_delete=models.SET_NULL,
		blank=True,
		null=True,
		related_name="intake_agents",
		help_text="Required for intake agents. Link to organization account user.",
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username} ({self.role})"



class DoctorProfile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="doctor_profile",
	)
	phone_number = models.CharField(max_length=20, blank=True)
	email = models.EmailField(blank=True)
	address = models.TextField(blank=True)
	state = models.CharField(
		max_length=50,
		choices=states,
		blank=True
	)
	postal_code = models.CharField(max_length=20, blank=True)
	
	npi = models.CharField(max_length=100, blank=True)

	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"Dr. {self.user.first_name} {self.user.last_name} - {self.npi}"


class DoctorLicense(models.Model):
	doctor = models.ForeignKey(
		DoctorProfile,
		on_delete=models.CASCADE,
		related_name="licenses"
	)
	license_number = models.CharField(max_length=50)
	license_state = models.CharField(
		max_length=50,
		choices=states
	)	
	expiration_date = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.doctor.user.username} - {self.license_number} ({self.license_state})"

	