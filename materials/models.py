"""
Materials Models — Study material uploads for NS Classes.
"""
from django.db import models
from django.contrib.auth.models import User
from courses.models import Subject
from batches.models import Batch


class StudyMaterial(models.Model):
    """Uploaded study material (PDF, assignments, etc.)."""
    TYPE_CHOICES = [
        ('notes', 'PDF Notes'),
        ('assignment', 'Assignment'),
        ('practice', 'Practice Paper'),
        ('important', 'Important Questions'),
        ('sample', 'Sample Paper'),
        ('other', 'Other'),
    ]
    BOARD_CHOICES = [
        ('CBSE', 'CBSE Board'),
    ]
    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(6, 13)]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    material_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='notes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='materials')
    class_level = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class', blank=True)
    board = models.CharField(max_length=10, choices=BOARD_CHOICES, blank=True)
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='materials')
    file = models.FileField(upload_to='materials/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_materials')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.get_material_type_display()})"

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Study Material'
        verbose_name_plural = 'Study Materials'
