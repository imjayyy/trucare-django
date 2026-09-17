from django.contrib import admin
from .models import PrescribeAbleItem, Script, ScriptItem, ScriptClientRelationship, LetterOfMedicalNecessity




class PrescribeAbleItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'item_type', 'active', 'quantity', 'refills')
    list_filter = ('category', 'item_type', 'active')
    search_fields = ('name', 'generic_name')


class LetterOfMedicalNecessityAdmin(admin.ModelAdmin):
    list_display = ('title', 'prescribeable_item', 'surgical', 'included_in_script', 'date_created')
    list_filter = ('surgical', 'included_in_script', 'date_created')
    search_fields = ('prescribeable_item__name',)

class ScriptItemAdmin(admin.ModelAdmin):
    list_display = ('script', 'prescribeable_item', 'prescribeable_item__category')
    list_filter = ('script', 'prescribeable_item__category')
    search_fields = ('script__id', 'prescribeable_item__name')

admin.site.register(PrescribeAbleItem, PrescribeAbleItemAdmin)
admin.site.register(Script)
admin.site.register(ScriptItem, ScriptItemAdmin)
admin.site.register(ScriptClientRelationship)   
admin.site.register(LetterOfMedicalNecessity, LetterOfMedicalNecessityAdmin)