from django.contrib import admin
from .models import Teacher

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'full_name', 'phone', 'email', 'qualification', 'experience', 'joining_date', 'is_active')
    list_filter = ('is_active', 'joining_date')
    search_fields = ('teacher_id', 'user__first_name', 'user__last_name', 'user__email', 'phone', 'qualification')
    filter_horizontal = ('specialization',)
    list_editable = ('is_active',)
