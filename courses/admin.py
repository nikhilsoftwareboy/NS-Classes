from django.contrib import admin
from .models import Subject, Course

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'icon')
    search_fields = ('name', 'code')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'class_level', 'duration', 'fees', 'is_active', 'created_at')
    list_filter = ('board', 'class_level', 'is_active')
    search_fields = ('name', 'description')
    filter_horizontal = ('subjects',)
    list_editable = ('is_active', 'fees')
