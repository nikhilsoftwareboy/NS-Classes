from django.contrib import admin
from .models import TimetableEntry

@admin.register(TimetableEntry)
class TimetableEntryAdmin(admin.ModelAdmin):
    list_display = ('batch', 'day', 'subject', 'teacher', 'start_time', 'end_time', 'room')
    list_filter = ('day', 'batch__board', 'batch', 'teacher')
    search_fields = ('batch__name', 'subject__name', 'teacher__user__first_name', 'room')
