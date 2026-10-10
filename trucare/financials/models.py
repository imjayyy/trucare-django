from django.db import models

from accounts.models import AccountProfile

# Create your models here.

class DoctorConsults(models.Model):
    doctor = models.ForeignKey(
        "accounts.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="consults",
    )

    patient = models.ForeignKey(
        "intake.PatientIntake",
        on_delete=models.CASCADE,
        related_name="consults",
    )

    consult_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost per consult in USD")

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Consult for Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}"

    
class DoctorConsultCost(models.Model):
    doctor = models.OneToOneField(
        "accounts.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="consult_cost",
        unique=True
    )
    consult_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost per consult in USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consult Cost for Dr. {self.doctor.user.first_name} {self.doctor.user.last_name}"



class ClientCredit(models.Model):
    client = models.ForeignKey(
        "accounts.AccountProfile",
        on_delete=models.CASCADE,
        related_name="client_credits",
        unique=True
    )
    credits = models.PositiveIntegerField(default=0)
    credit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost per credit in USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client Credit for {self.client.user.first_name} {self.client.user.last_name}"


class ClientCreditRecord(models.Model):
    client = models.ForeignKey(
        "accounts.AccountProfile",
        on_delete=models.CASCADE,
        related_name="credit_records",
    )

    intake = models.ForeignKey(
        "intake.PatientIntake",
        on_delete=models.CASCADE,
        related_name="credit_records",
    )
    credit_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost per credit in USD")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Client Credit Record for Intake ID {self.intake.id} (Client: {self.client.user.first_name} {self.client.user.last_name})"

    def save(self, *args, **kwargs):
        if not self.credit_cost:
            self.credit_cost = 0.00
        
        credits = ClientCredit.objects.filter(client=self.client).first()
        if credits:
            if credits.credits > 0:
                credits.credits -= 1
                self.credit_cost = credits.credit_cost
                credits.save()
            else:
                raise ValueError("Insufficient credits for the client.")
        super().save(*args, **kwargs)



    
def add_doctor_consult(doctor, patient):
    consult_cost_object = DoctorConsultCost.objects.filter(doctor=doctor).first()
    client = patient.client
    
    if consult_cost_object:
        consult_cost = consult_cost_object.consult_cost
    else:
        consult_cost = 0.00

    DoctorConsults.objects.create(
        doctor=doctor,
        patient=patient,
        consult_cost=consult_cost
    )
    client_profile = AccountProfile.objects.filter(user=client).first()
    ClientCreditRecord.objects.create(client=client_profile, intake=patient)

    return True
