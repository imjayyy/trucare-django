from django.db import models

from intake.models import Condition



class PrescribeAbleItem(models.Model):

    MEDICATION = "medication"
    THERAPY = "therapy"
    DEVICE = "device"
    SUPPLEMENT = "supplement"
    ITEM_TYPES = [
        (MEDICATION, "Medication"),
        (THERAPY, "Therapy"),
        (DEVICE, "Device"),
        (SUPPLEMENT, "Supplement"),
    ]
    category = models.ForeignKey(
        Condition,
        on_delete=models.PROTECT,
        related_name="items",
    )
    item_type = models.CharField(
        max_length=20,
        choices=ITEM_TYPES
    )
    name = models.CharField(max_length=255)
    generic_name = models.CharField(
        max_length=255,
        blank=True
    )
    strength = models.CharField(
        max_length=100,
        blank=True
    )
    dosage_form = models.CharField(
        max_length=100,
        blank=True,
        help_text="Tablet, Capsule, Cream, Gel..."
    )

    usual_sig = models.TextField(
        blank=True,
        help_text="Apply 1-2 grams to affected area BID"
    )

    quantity = models.CharField(
        max_length=100,
        blank=True
    )

    refills = models.PositiveIntegerField(default=0)

    duration = models.CharField(
        max_length=100,
        blank=True
    )

    description = models.TextField(blank=True)

    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name
    

class Script(models.Model):
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name



class ScriptItem(models.Model):
    script = models.ForeignKey(
        Script,
        on_delete=models.CASCADE,
        related_name="script_items"
    )
    prescribeable_item = models.ForeignKey(
        PrescribeAbleItem,
        on_delete=models.PROTECT,
        related_name="script_items"
    )

    def __str__(self):
        return f"{self.prescribeable_item.name} in {self.script.name}"

class ScriptClientRelationship(models.Model):
    script = models.ForeignKey(
        Script,
        on_delete=models.CASCADE,
        related_name="client_relationships"
    )
    client = models.ForeignKey(
        "accounts.AccountProfile",
        on_delete=models.CASCADE,
        related_name="script_relationships"
    )

    class Meta:
        unique_together = ("script", "client")

    def __str__(self):
        return f"{self.client.user.username} has access to {self.script.name}"


