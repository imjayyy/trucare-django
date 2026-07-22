from django.db import models


class PrescriptionCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name
    

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
        PrescriptionCategory,
        on_delete=models.PROTECT,
        related_name="items"
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
    prescribeable_item = models.ForeignKey(
        PrescribeAbleItem,
        on_delete=models.PROTECT,
        related_name="scripts"
    )
    
    class Meta:
        unique_together = ("name", "prescribeable_item")
    
    def __str__(self):
        return self.name