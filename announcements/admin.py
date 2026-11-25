from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'target_audience', 'batch', 'priority', 'date', 'created_by', 'is_active')
    list_filter = ('target_audience', 'priority', 'is_active', 'date')
    search_fields = ('title', 'description')
    list_editable = ('is_active', 'priority')
    date_hierarchy = 'date'
