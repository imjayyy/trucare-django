from django.contrib import admin
from .models import (
	Choice,
	ChoiceSet,
	Condition,
	ConditionQuestion,
	Health_Record,
	Insurance,
	Medical_History,
	Patient_Info,
	PatientAnswer,
	PatientAnswerChoice,
	PatientCondition,
	Patient_Family_History,
)

class ConditionQuestionAdmin(admin.ModelAdmin):
    list_display = ('id', 'question', 'condition', 'order')
    list_filter = ('condition',)
    search_fields = ('question',)

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'choice_set', 'text')
    list_filter = ('choice_set',)
    search_fields = ('text',)

admin.site.register(Patient_Info)
admin.site.register(Insurance)
admin.site.register(Medical_History)
admin.site.register(Health_Record)
admin.site.register(Patient_Family_History)
admin.site.register(ChoiceSet)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Condition)
admin.site.register(PatientCondition)
admin.site.register(ConditionQuestion, ConditionQuestionAdmin)
admin.site.register(PatientAnswer)
admin.site.register(PatientAnswerChoice)

