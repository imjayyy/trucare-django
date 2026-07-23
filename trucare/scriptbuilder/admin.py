from django.contrib import admin
from .models import PrescribeAbleItem, Script, ScriptItem, ScriptClientRelationship




class PrescribeAbleItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'item_type', 'active')
    list_filter = ('category', 'item_type', 'active')
    search_fields = ('name', 'generic_name', 'strength', 'dosage_form')


admin.site.register(PrescribeAbleItem, PrescribeAbleItemAdmin)
admin.site.register(Script)
admin.site.register(ScriptItem)
admin.site.register(ScriptClientRelationship)