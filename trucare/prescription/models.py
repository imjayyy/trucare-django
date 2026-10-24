from django.db import models
from scriptbuilder.models import PrescribeAbleItem, Script
from intake.models import Condition, ConditionQuestion, Insurance, PatientIntake, PatientInfo, states
# Create your models here.
from scriptbuilder.models import PrescribeAbleItem
import os
from django.utils import timezone


def prescription_upload_path(instance, filename):
    # 1. Extract file extension
    _, extension = os.path.splitext(filename)
    
    # 2. Get high-precision timestamp
    timestamp = timezone.now().strftime("%Y%m%d_%H%M%S_%f")
    
    # 3. Create chronological subfolders to prevent folder congestion
    year_month = timezone.now().strftime("%Y/%m")
    
    # 4. Build the unique path using the guaranteed object ID
    # Example path: prescriptions/2026/09/rx_145_20260901_045712_123456.pdf
    new_filename = f"rx_{instance.pk}_{timestamp}{extension}"
    return os.path.join('prescriptions', year_month, new_filename)


class Prescription(models.Model):
    patient = models.ForeignKey(
        PatientIntake,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    doctor = models.ForeignKey(
        "accounts.DoctorProfile",
        on_delete=models.SET_NULL,
        null=True,
        related_name="prescriptions"
    )
    script = models.ForeignKey(
        Script,
        on_delete=models.SET_NULL,
        null=True,
        related_name="prescriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pdf_file = models.FileField(
        upload_to=prescription_upload_path,
        blank=True,
        null=True)
    def __str__(self):
        return f"Prescription for {self.patient}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items"
    )
    category = models.ForeignKey(Condition, on_delete=models.PROTECT)
    item_type = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255, blank=True, null=True)
    ndc = models.CharField(max_length=100, blank=True, null=True)
    strength = models.CharField(max_length=100, blank=True)
    dosage_form = models.CharField(max_length=100, blank=True)
    usual_sig = models.TextField(blank=True)
    quantity = models.CharField(max_length=100, blank=True)
    refills = models.PositiveIntegerField(default=0)
    duration = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    instructions = models.TextField(blank=True)
    requires_letter_of_medical_necessity = models.BooleanField(default=False, 
                                                               help_text="Indicates if this item requires a letter of medical necessity.")

    letter_of_medical_necessity = models.ForeignKey(
        "scriptbuilder.LetterOfMedicalNecessity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prescription_items"
    )

    show_in_script = models.BooleanField(
            default=True,
            help_text="Indicates if this item should be shown in the script."
        )

    def __str__(self):
        return f"{self.name} for {self.prescription.patient}"


class PrimaryDrug(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="primary_drugs"
    )
    drug = models.ForeignKey(
        PrescriptionItem,
        on_delete=models.CASCADE,
        related_name="primary_drug_prescriptions"
    )

    def __str__(self):
        return f"{self.drug.name} for {self.prescription.patient}"


class SecondaryDrug(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="secondary_drugs"
    )
    drug = models.ForeignKey(
        PrescriptionItem,
        on_delete=models.CASCADE,
        related_name="secondary_drug_prescriptions"
    )

    def __str__(self):
        return f"{self.drug.name} for {self.prescription.patient}"




class Soap_notes(models.Model):
    patient_intake = models.ForeignKey(
        PatientIntake,
        on_delete=models.CASCADE,
        related_name="soap_notes",
        null=True,
        blank=True,
        unique=True,
    )
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)

    def __str__(self):
        return f"SOAP notes for {self.patient_intake}"


    class Meta:
        verbose_name = "SOAP Note"
        verbose_name_plural = "SOAP Notes"
        