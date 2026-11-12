from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
from intake.models import states


User = get_user_model()


class AccountProfile(models.Model):
	ROLE_ADMIN = "ADMIN"
	ROLE_MANAGER = "MANAGER"
	ROLE_ORGANIZATION = "ORGANIZATION"
	ROLE_INTAKE_AGENT = "INTAKE_AGENT"
	ROLE_BILLING = "BILLING"
	ROLE_DOCTOR = "DOCTOR"
	ROLE_PHARMACY = "PHARMACY"

	ROLE_CHOICES = [
		(ROLE_ADMIN, "Admin"),
		(ROLE_MANAGER, "Manager"),
		(ROLE_ORGANIZATION, "Organization"),
		(ROLE_INTAKE_AGENT, "Intake Agent"),
		(ROLE_BILLING, "Billing"),
		(ROLE_DOCTOR, "Doctor"),
		(ROLE_PHARMACY, "Pharmacy"),
		
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


class AgencyProfile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="agency_profile",
	)
	"""Contact No, Fax, Website, Prim contact, prime email, prim phone, address, state, zip code"""

	phone_number = models.CharField(max_length=20, blank=True)
	email = models.EmailField(blank=True)
	address = models.TextField(blank=True)
	state = models.CharField(
		max_length=50,
		choices=states,
		blank=True
	)
	postal_code = models.CharField(max_length=20, blank=True)
	website = models.URLField(blank=True)
	fax_number = models.CharField(max_length=20, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)	

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		account_profile = AccountProfile.objects.get(user=self.user)
		if not account_profile:
			raise ValueError("User must have an AccountProfile to create an AgencyProfile.")
		if account_profile.role != AccountProfile.ROLE_ORGANIZATION:
			raise ValueError("User must have role 'ORGANIZATION' to create an AgencyProfile.")

		return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)


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
	signature = models.ImageField(
		upload_to='doctor_signatures/',
		blank=True,
		null=True,
		validators=[FileExtensionValidator(allowed_extensions=['png'])],
	)
	
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

class LegacyIdMap(models.Model):
	"""Two-way link between a legacy Mongo ObjectId and a Django object id."""
	collection = models.CharField(max_length=50)
	mongo_id = models.CharField(max_length=24)
	object_id = models.PositiveIntegerField()

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=["collection", "mongo_id"], name="uniq_legacy_mongo_id"),
			models.UniqueConstraint(fields=["collection", "object_id"], name="uniq_legacy_object_id"),
		]

	def __str__(self):
		return f"{self.collection}: {self.mongo_id} <-> {self.object_id}"


class PharmacyProfile(models.Model):
	user = models.OneToOneField(
		User,
		on_delete=models.CASCADE,
		related_name="pharmacy_profile",
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
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.user.username} ({self.user.first_name} {self.user.last_name})"

	# def save(self, *args, **kwargs):
	# 	if self.user.account_profile.role
	# 	if not self.state:
	# 		self.state = "N/A"
	# 	super().save(*args, **kwargs)