from django.contrib import admin
from .models import AccountProfile, DoctorLicense, DoctorProfile, AgencyProfile

admin.site.register(AccountProfile)
admin.site.register(DoctorLicense)
admin.site.register(DoctorProfile)
admin.site.register(AgencyProfile)  # Register the AgencyProfile model with the admin site
admin.site.site_header = "Trucare Admin"
