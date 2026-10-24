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
        blank=True,
        null=True,
    )
    ndc = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="National Drug Code (NDC) for medications."
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

    show_in_script = models.BooleanField(
        default=True,
        help_text="Indicates if this item should be shown in the script."
    )
    requires_letter_of_medical_necessity = models.BooleanField(
        default=False,
        help_text="Indicates if this item requires a letter of medical necessity."
    )
    letter_of_medical_necessity = models.ForeignKey(
        "LetterOfMedicalNecessity",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prescribeable_items"
    )
    
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
        related_name="script_relationships",
        unique=True
    )


    def __str__(self):
        return f"{self.client.user.username} has access to {self.script.name}"


class ScriptIntakeRelationship(models.Model):
    script = models.ForeignKey(
        Script,
        on_delete=models.CASCADE,
        related_name="intake_relationships"
        
    )
    intake = models.ForeignKey(
        "intake.PatientIntake",
        on_delete=models.CASCADE,
        related_name="script_relationships",
        unique=True
    )

    def __str__(self):
        return f"{self.intake.id} has access to {self.script.name}"

    class Meta:
        ordering = ["intake", "script"]
        unique_together = ["intake", "script"]


class LetterOfMedicalNecessity(models.Model):
    prescribeable_item = models.ForeignKey(
        PrescribeAbleItem,
        on_delete=models.PROTECT,
        related_name="letters_of_medical_necessity"
    )
    title = models.CharField(
        max_length=255,
        help_text="The title of the letter of medical necessity.",
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        help_text="A brief description of the letter of medical necessity."
    )


    surgical = models.BooleanField(
        default=False,
        help_text="Indicates if this letter is for a surgical procedure."
    )
    included_in_script = models.BooleanField(
        default=True,
        help_text="Indicates if this letter is included in the script."
    )
    include_doctors_information = models.BooleanField(
        default=True,
        help_text="Indicates if the doctor's information should be included in the letter."
    )
    include_condition_questionnaire = models.BooleanField(
        default=True,
        help_text="Indicates if the condition questionnaire should be included in the letter."
    )
    include_treatment_plan = models.BooleanField(
        default=True,
        help_text="Indicates if the treatment plan should be included in the letter."
    )

    letter_content_html = models.TextField(
        blank=True,
        help_text="""The content of the letter of medical necessity. 
                    This can include HTML formatting. 
                    Add <br/> for line breaks (New Paragraph)."""    )

    custom_logo_upload = models.ImageField(
        upload_to="custom_logos_for_letters/",
        blank=True,
        help_text="Upload a custom logo to be included in the letter."
    )
    
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Letter of Medical Necessity for {self.prescribeable_item.name}"


    def save(self, *args, **kwargs):
        self.prescribeable_item.letter_of_medical_necessity = self
        self.prescribeable_item.save()
        super().save(*args, **kwargs)