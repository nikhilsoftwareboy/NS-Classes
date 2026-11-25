"""
Courses Models — Subject and Course management for NS Classes.
"""
from django.db import models


class Subject(models.Model):
    """Academic subject (Math, Science, etc.)."""
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text='Bootstrap icon class e.g. bi-calculator')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Course(models.Model):
    """Course offered by NS Classes."""
    BOARD_CHOICES = [
        ('CBSE', 'CBSE Board'),
    ]
    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(6, 13)]

    name = models.CharField(max_length=200)
    description = models.TextField()
    board = models.CharField(max_length=10, choices=BOARD_CHOICES)
    class_level = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class')
    subjects = models.ManyToManyField(Subject, related_name='courses')
    duration = models.CharField(max_length=50, help_text='e.g. 1 Year, 6 Months')
    fees = models.DecimalField(max_digits=10, decimal_places=2, help_text='Course fee in INR')
    image = models.ImageField(upload_to='courses/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_board_display()} - Class {self.class_level})"

    class Meta:
        ordering = ['board', 'class_level', 'name']
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
