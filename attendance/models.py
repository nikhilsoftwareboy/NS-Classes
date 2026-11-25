"""
Attendance Models — Student attendance tracking for NS Classes.
"""
from django.db import models
from django.contrib.auth.models import User
from students.models import Student
from batches.models import Batch


class Attendance(models.Model):
    """Daily attendance record for a student."""
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='present')
    marked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='marked_attendance')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"

    class Meta:
        ordering = ['-date', 'student']
        unique_together = ['student', 'date', 'batch']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
