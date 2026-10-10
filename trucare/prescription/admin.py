from django.contrib import admin
from .models import Prescription, PrescriptionItem, Soap_notes, PrimaryDrug, SecondaryDrug
# Register your models here.


class PrimaryDrugAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient_full_name',
        'drug__name',
        'drug__category__id',
        'drug__category__name',
    )

    list_filter = ('prescription',)

    search_fields = (
        'drug__name',
        'prescription__patient__patient__first_name',
        'prescription__patient__patient__last_name',
    )

    @admin.display(description='Full Name')
    def patient_full_name(self, obj):
        return f"{obj.prescription.patient.patient.first_name} {obj.prescription.patient.patient.last_name}"
    
class SecondaryDrugAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'patient_full_name',
        'drug__name',
        'drug__category__id',
        'drug__category__name',
    )
    list_filter = ('prescription',)
    search_fields = ('drug__name', 'prescription__patient__patient__first_name', 'prescription__patient__patient__last_name')

    @admin.display(description='Full Name')
    def patient_full_name(self, obj):
        return f"{obj.prescription.patient.patient.first_name} {obj.prescription.patient.patient.last_name}"

class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'patient_full_name', 'created_at', 'updated_at', "patient_id")
    list_filter = ('created_at', 'updated_at')
    search_fields = ('patient__patient__first_name', 'patient__patient__last_name')

    @admin.display(description='Full Name')
    def patient_full_name(self, obj):
        return f"{obj.patient.patient.first_name} {obj.patient.patient.last_name}"

    @admin.display(description='Intake ID')
    def patient_id(self, obj):
        return obj.patient.id

class PrescriptionItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'prescription', 'name', 'usual_sig')
    list_filter = ('prescription', 'prescription__patient__patient__first_name', 'prescription__patient__patient__last_name')
    search_fields = ('prescription__patient__patient__first_name', 'prescription__patient__patient__last_name', 'name')


admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(PrescriptionItem, PrescriptionItemAdmin)
admin.site.register(Soap_notes)
admin.site.register(PrimaryDrug, PrimaryDrugAdmin)
admin.site.register(SecondaryDrug, SecondaryDrugAdmin)
