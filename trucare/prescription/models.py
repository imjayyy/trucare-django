from django.db import models
from scriptbuilder.models import PrescribeAbleItem
from intake.models import Condition, ConditionQuestion, Insurance, Patient_Info
# Create your models here.


class Prescription(models.Model):
    patient = models.ForeignKey(
        Patient_Info,
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    doctor = models.ForeignKey(
        "accounts.User",
        on_delete=models.SET_NULL,
        null=True,
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