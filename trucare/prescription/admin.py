from django.contrib import admin
from .models import Prescription, PrescriptionItem, Soap_notes
# Register your models here.
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(Soap_notes)
