"""
Announcements Models — Notice and announcement system for NS Classes.
"""
from django.db import models
from django.contrib.auth.models import User
from batches.models import Batch


class Announcement(models.Model):
    """Announcement/notice for students and teachers."""
    AUDIENCE_CHOICES = [
        ('all', 'All Students'),
        ('batch', 'Specific Batch'),
        ('teachers', 'Teachers Only'),
    ]
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('important', 'Important'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    target_audience = models.CharField(max_length=10, choices=AUDIENCE_CHOICES, default='all')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='announcements',
                              help_text='Required if target is Specific Batch')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_priority_display()})"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
