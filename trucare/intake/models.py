from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

states = [
    ('AL', 'Alabama'),
    ('AK', 'Alaska'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming'),
]


Patient_Insurance_Choices = [
    ('Workmens_Compensation', 'Workmens Compensation'),
    ('RX_Insurance', 'RX Insurance'),
    ('PIP_Insurance', 'PIP Insurance')
]

class Patient_Info(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField()
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    state = models.CharField(choices=states, max_length=20, blank=True, null=True)
    
    client = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    intake_agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="intake_agent_patients",
        help_text="The intake agent who created this patient record.",
    )
    cordinator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="cordinator_patients",
        help_text="The cordinator who is assigned to this patient.",
    )
    doctor = models.ForeignKey(
        "accounts.DoctorProfile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="doctor_patients",
        help_text="The doctor who is assigned to this patient.",
    )

    status = models.CharField(max_length=50)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


""" Patient Insurance Information """

class Insurance(models.Model):

    INSURANCE_TYPES = [
        ("RX", "RX Insurance"),
        ("PIP", "PIP Insurance"),
        ("WC", "Workmen's Compensation"),
    ]

    patient = models.ForeignKey(
        Patient_Info,
        on_delete=models.CASCADE,
        related_name="insurances"
    )

    insurance_type = models.CharField(
        max_length=5,
        choices=INSURANCE_TYPES
    )

    primary_insured = models.BooleanField(default=False)

    # Common fields
    insurance_carrier = models.CharField(max_length=100, blank=True, null=True)
    carrier_phone = models.CharField(max_length=15, blank=True, null=True)

    # RX fields
    group_id = models.CharField(max_length=50, blank=True, null=True)
    patient_id_rx = models.CharField(max_length=50, blank=True, null=True)
    bin = models.CharField(max_length=20, blank=True, null=True)
    pcn = models.CharField(max_length=20, blank=True, null=True)

    # PIP / WC common
    adjuster_name = models.CharField(max_length=100, blank=True, null=True)
    adjuster_phone = models.CharField(max_length=15, blank=True, null=True)

    # PIP
    policy_number = models.CharField(max_length=50, blank=True, null=True)
    claim_number = models.CharField(max_length=100, blank=True, null=True)
    date_of_accident = models.DateField(blank=True, null=True)

    # Workmen's Compensation
    payer_name = models.CharField(max_length=100, blank=True, null=True)
    date_of_injury = models.DateField(blank=True, null=True)
    employer_name = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        """
        Optional: validate fields depending on insurance_type.
        """
        from django.core.exceptions import ValidationError

        if self.insurance_type == "RX":
            required = ["insurance_carrier", "group_id", "patient_id_rx", "bin", "pcn"]
        elif self.insurance_type == "PIP":
            required = ["insurance_carrier", "policy_number"]
        elif self.insurance_type == "WC":
            required = ["payer_name", "claim_number", "date_of_injury"]
        else:
            required = []

        errors = {}
        for field in required:
            if not getattr(self, field):
                errors[field] = "This field is required."

        if errors:
            raise ValidationError(errors)



""" Patient Insurance Information """

class Medical_History(models.Model):
    patient = models.ForeignKey(Patient_Info, on_delete=models.CASCADE, related_name='medical_histories')
    condition = models.CharField(max_length=100)
    diagnosis_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.condition} for {self.patient.first_name} {self.patient.last_name}"
    

class Health_Record(models.Model):
    patient = models.ForeignKey(Patient_Info, on_delete=models.CASCADE, related_name='health_records')
    record_type = models.CharField(max_length=100, choices=[
        ('Medical Conditions', 'Medical Conditions'),
        ('Allergies', 'Allergies'),
        ('Surgeries', 'Surgeries'),
        ('Medications', 'Medications'),
        ('Other', 'Other'), 

    ])
    record_date = models.DateField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.record_type} for {self.patient.first_name} {self.patient.last_name}"
    
class Patient_Family_History(models.Model):
    """Model to store family medical history for a patient.
    """
    patient = models.ForeignKey(Patient_Info, on_delete=models.CASCADE, related_name='family_histories')
    asthama = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    bleeding_tendency = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    cancer = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    colitis = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    depression = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    diabetes = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    epilepsy = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    heart_attack = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    high_blood_pressure = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    kidney_disease = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    leukemia = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    migraine = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    schizophrenia = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    stomach_ulcers = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    stroke = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')   
    suicide = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')
    tuberculosis = models.CharField(max_length=20, choices=[('None', 'None'), ('Unknown', 'Unknown'), ('Yes', 'Yes')], default='None')  



class ChoiceSet(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Choice(models.Model):
    choice_set = models.ForeignKey(
        ChoiceSet,
        on_delete=models.CASCADE,
        related_name="choices"
    )

    text = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=1)
    icd_code = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        ordering = ["order"]
        unique_together = ("choice_set", "text")

    def __str__(self):
        return self.text


class Condition(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=30, unique=True)
    icd_code = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name


class PatientCondition(models.Model):
    patient = models.ForeignKey(
        Patient_Info,
        on_delete=models.CASCADE,
        related_name="requested_conditions"
    )

    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name="patients"
    )

    requested = models.BooleanField(default=False)

    class Meta:
        unique_together = ("patient", "condition")


class ConditionQuestion(models.Model):

    TEXT = "text"
    YES_NO = "yes_no"
    NUMBER = "number"
    DATE = "date"
    SINGLE_CHOICE = "single_choice"
    MULTIPLE_CHOICE = "multiple_choice"

    QUESTION_TYPES = [
        (TEXT, "Text"),
        (YES_NO, "Yes / No"),
        (NUMBER, "Number"),
        (DATE, "Date"),
        (SINGLE_CHOICE, "Single Choice"),
        (MULTIPLE_CHOICE, "Multiple Choice"),
    ]

    condition = models.ForeignKey(
        Condition,
        on_delete=models.CASCADE,
        related_name="questions"
    )

    question = models.TextField()

    question_type = models.CharField(
        max_length=30,
        choices=QUESTION_TYPES
    )

    # Only used for choice questions
    choice_set = models.ForeignKey(
        ChoiceSet,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="questions"
    )

    required = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.question


class PatientAnswer(models.Model):
    patient = models.ForeignKey(
        Patient_Info,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    question = models.ForeignKey(
        ConditionQuestion,
        on_delete=models.CASCADE,
        related_name="answers"
    )

    text_answer = models.TextField(blank=True, null=True)
    number_answer = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True
    )
    boolean_answer = models.BooleanField(blank=True, null=True)
    date_answer = models.DateField(blank=True, null=True)

    class Meta:
        unique_together = ("patient", "question")


class PatientAnswerChoice(models.Model):
    answer = models.ForeignKey(
        PatientAnswer,
        on_delete=models.CASCADE,
        related_name="selected_choices"
    )

    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name="selected_answers"
    )

    class Meta:
        unique_together = ("answer", "choice")