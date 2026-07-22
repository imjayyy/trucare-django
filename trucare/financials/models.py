from django.db import models

# Create your models here.

class DoctorConsults(models.Model):
    doctor = models.ForeignKey(
        "accounts.DoctorProfile",
        on_delete=models.CASCADE,
        related_name="consults",
        unique=True
    )
    credits = models.PositiveIntegerField(default=0)
    consult_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Cost per consult in USD")

    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Consult for Dr. {self.doctor.first_name} {self.doctor.last_name}"


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
        return f"Client Credit for {self.client.first_name} {self.client.last_name}"

