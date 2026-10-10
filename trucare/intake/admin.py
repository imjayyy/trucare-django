from django.contrib import admin
from django import forms

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

class ConditionQuestionAdminForm(forms.ModelForm):

    class Meta:
        model = ConditionQuestion
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only YES/NO questions can be used as dependencies
        qs = ConditionQuestion.objects.filter(
            question_type=ConditionQuestion.YES_NO,
			condition=self.instance.condition if self.instance and self.instance.pk else None
        )

        # When editing an existing question, restrict to same condition
        if self.instance and self.instance.pk:
            qs = qs.filter(
                condition=self.instance.condition
            )

        # Exclude itself
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        self.fields["show_when"].queryset = qs

		
class ConditionQuestionAdmin(admin.ModelAdmin):
    form = ConditionQuestionAdminForm
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


class PatientIntakeAdmin(admin.ModelAdmin):
	list_display = ('id', 'patient', 'patient__date_of_birth', 'patient__email', 'patient__phone_number', 'status', 'updated_at')
	list_filter = ('updated_at', 'status', 'created_at', 'doctor')
	search_fields = ('patient__first_name', 'id', 'patient__id', 'patient__email')


admin.site.register(PatientIntake, PatientIntakeAdmin)
admin.site.register(PatientInfo)
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

