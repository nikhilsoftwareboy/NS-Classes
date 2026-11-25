from django.contrib import admin
from .models import Batch

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'board', 'class_level', 'teacher', 'start_date', 'end_date', 'current_students_count', 'max_students', 'status')
    list_filter = ('board', 'class_level', 'status', 'teacher')
    search_fields = ('name', 'course__name')
    filter_horizontal = ('subjects',)
    list_editable = ('status',)

    def current_students_count(self, obj):
        return obj.current_students
    current_students_count.short_description = 'Students Enrolled'
