from django.contrib import admin
from .models import PrescribeAbleItem, PrescriptionCategory, Script

admin.site.register(PrescriptionCategory)
admin.site.register(PrescribeAbleItem)
admin.site.register(Script)
