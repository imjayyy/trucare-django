from django.contrib import admin
from .models import AccountProfile, DoctorLicense, DoctorProfile

admin.site.register(AccountProfile)
admin.site.register(DoctorLicense)
admin.site.register(DoctorProfile)