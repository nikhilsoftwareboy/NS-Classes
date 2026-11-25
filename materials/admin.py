from django.contrib import admin
from .models import StudyMaterial

@admin.register(StudyMaterial)
class StudyMaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'material_type', 'subject', 'board', 'class_level', 'batch', 'uploaded_by', 'upload_date')
    list_filter = ('material_type', 'board', 'class_level', 'subject', 'upload_date')
    search_fields = ('title', 'description', 'subject__name', 'batch__name')
    date_hierarchy = 'upload_date'
