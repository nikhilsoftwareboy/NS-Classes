from django.contrib import admin
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'full_name', 'roll_number', 'board', 'class_level', 'course', 'batch', 'phone', 'is_active')
    list_filter = ('board', 'class_level', 'course', 'batch', 'is_active', 'gender')
    search_fields = ('student_id', 'roll_number', 'user__first_name', 'user__last_name', 'user__email', 'phone', 'parent_phone', 'father_name')
    list_editable = ('is_active',)
    raw_id_fields = ('user',)
