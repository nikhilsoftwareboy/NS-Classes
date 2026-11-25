from django.contrib import admin
from .models import FeeRecord

@admin.register(FeeRecord)
class FeeRecordAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'student', 'total_fee', 'paid_amount', 'remaining_display', 'status', 'payment_date', 'payment_method')
    list_filter = ('status', 'payment_method', 'payment_date')
    search_fields = ('receipt_number', 'student__user__first_name', 'student__user__last_name', 'student__student_id')
    readonly_fields = ('receipt_number', 'status', 'created_at', 'updated_at')

    def remaining_display(self, obj):
        return f"₹{obj.remaining_amount}"
    remaining_display.short_description = 'Remaining'
