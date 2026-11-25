from django.contrib import admin
from .models import Attendance

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'batch', 'date', 'status', 'marked_by', 'created_at')
    list_filter = ('status', 'date', 'batch')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__student_id', 'batch__name')
    date_hierarchy = 'date'
