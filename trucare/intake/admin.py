from django.contrib import admin
from .models import (
	Choice,
	ChoiceSet,
	Condition,
	ConditionQuestion,
	HealthRecord,
	Insurance,
	MedicalHistory,
	PatientInfo,
	PatientAnswer,
	PatientAnswerChoice,
	PatientCondition,
	PatientFamilyHistory,
	PatientIntake,
)

class ConditionQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'condition', 'question_type', 'order')
    list_filter = ('condition',)
    search_fields = ('question',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_set', 'text')
    list_filter = ('choice_set',)
    search_fields = ('text',)

class PatientConditionAdmin(admin.ModelAdmin):
	list_display = ('id', 'patient', 'condition', 'requested')
	list_filter = ('condition', 'requested')
	search_fields = ('patient__first_name', 'patient__last_name', 'condition__name', 'patient__id')

admin.site.register(PatientInfo)
admin.site.register(PatientIntake)
admin.site.register(Insurance)
admin.site.register(MedicalHistory)
admin.site.register(HealthRecord)
admin.site.register(PatientFamilyHistory)
admin.site.register(ChoiceSet)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Condition)
admin.site.register(PatientCondition, PatientConditionAdmin)
admin.site.register(ConditionQuestion, ConditionQuestionAdmin)
admin.site.register(PatientAnswer)
admin.site.register(PatientAnswerChoice)

