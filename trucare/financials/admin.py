from django.contrib import admin
from .models import ClientCreditRecord, ClientCredit, DoctorConsultCost, DoctorConsults


admin.site.register(ClientCreditRecord)
admin.site.register(ClientCredit)
admin.site.register(DoctorConsultCost)
admin.site.register(DoctorConsults)
# Register your models here.
