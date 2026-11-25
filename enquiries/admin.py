from django.contrib import admin
from .models import AdmissionEnquiry, ContactMessage

@admin.register(AdmissionEnquiry)
class AdmissionEnquiryAdmin(admin.ModelAdmin):
    list_display = ('student_name', 'parent_name', 'phone', 'email', 'board', 'class_level', 'status', 'created_at')
    list_filter = ('status', 'board', 'class_level', 'created_at')
    search_fields = ('student_name', 'parent_name', 'phone', 'email', 'interested_course')
    list_editable = ('status',)
    date_hierarchy = 'created_at'

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    list_editable = ('is_read',)
    date_hierarchy = 'created_at'
