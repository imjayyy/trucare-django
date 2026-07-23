from django.db import models
from scriptbuilder.models import PrescribeAbleItem, Script
from intake.models import Condition, ConditionQuestion, Insurance, Patient_Info
# Create your models here.


class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient_Info,
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
        on_delete=models.PROTECT,
        related_name="prescriptions"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Prescription for {self.patient}"

class PrescriptionItem(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="items"
    )
    prescribeable_item = models.ForeignKey(
        "scriptbuilder.PrescribeAbleItem",
        on_delete=models.PROTECT,
        related_name="prescription_items"
    )
    quantity = models.PositiveIntegerField()
    instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.prescribeable_item.name} for {self.prescription.patient}"


class Soap_notes(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name="soap_notes"
    )
    subjective = models.TextField(blank=True)
    objective = models.TextField(blank=True)
    assessment = models.TextField(blank=True)
    plan = models.TextField(blank=True)

    def __str__(self):
        return f"SOAP notes for {self.prescription.patient}"


    