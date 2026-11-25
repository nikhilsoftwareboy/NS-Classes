"""
Batches Models — Batch management for NS Classes.
"""
from django.db import models
from courses.models import Course, Subject
from teachers.models import Teacher


class Batch(models.Model):
    """A study batch grouping students together."""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('upcoming', 'Upcoming'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    BOARD_CHOICES = [
        ('CBSE', 'CBSE Board'),
    ]
    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(6, 13)]

    name = models.CharField(max_length=200)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    board = models.CharField(max_length=10, choices=BOARD_CHOICES)
    class_level = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class')
    subjects = models.ManyToManyField(Subject, related_name='batches', blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='batches')
    start_date = models.DateField()
    end_date = models.DateField()
    max_students = models.PositiveIntegerField(default=30)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def current_students(self):
        return self.students.count()

    @property
    def is_full(self):
        return self.current_students >= self.max_students

    class Meta:
        ordering = ['name']
        verbose_name = 'Batch'
        verbose_name_plural = 'Batches'
