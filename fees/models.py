"""
Fees Models — Fee management for NS Classes.
"""
from django.db import models
from students.models import Student
import uuid


class FeeRecord(models.Model):
    """Fee payment record for a student."""
    STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('pending', 'Pending'),
        ('overdue', 'Overdue'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('bank', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('online', 'Online Payment'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fee_records')
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, blank=True)
    receipt_number = models.CharField(max_length=50, unique=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = f"NS-{uuid.uuid4().hex[:8].upper()}"
        # Auto-calculate status
        if self.paid_amount >= self.total_fee:
            self.status = 'paid'
        elif self.paid_amount > 0:
            self.status = 'partial'
        super().save(*args, **kwargs)

    @property
    def remaining_amount(self):
        return self.total_fee - self.paid_amount

    def __str__(self):
        return f"{self.student} - ₹{self.paid_amount}/{self.total_fee} ({self.get_status_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Fee Record'
        verbose_name_plural = 'Fee Records'
