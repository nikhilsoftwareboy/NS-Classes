"""
Timetable Models — Per-batch timetable entries for NS Classes.
"""
from django.db import models
from batches.models import Batch
from courses.models import Subject
from teachers.models import Teacher


class TimetableEntry(models.Model):
    """A single timetable slot for a batch."""
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='timetable_entries')
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetable_entries')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetable_entries')
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=20, blank=True, help_text='Room number')

    def __str__(self):
        return f"{self.batch.name} - {self.day} - {self.subject.name} ({self.start_time}-{self.end_time})"

    class Meta:
        ordering = ['batch', 'day', 'start_time']
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable Entries'
