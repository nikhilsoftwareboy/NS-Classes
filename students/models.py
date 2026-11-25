"""
Students Models — Student profiles for NS Classes.
"""
from django.db import models
from django.contrib.auth.models import User
from courses.models import Course
from batches.models import Batch


class Student(models.Model):
    """Student profile linked to a Django User."""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    BOARD_CHOICES = [
        ('CBSE', 'CBSE Board'),
    ]
    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(6, 13)]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='students/', blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    father_name = models.CharField(max_length=100, blank=True)
    mother_name = models.CharField(max_length=100, blank=True)
    phone = models.CharField(max_length=15, blank=True)
    parent_phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    board = models.CharField(max_length=10, choices=BOARD_CHOICES, blank=True)
    class_level = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class', blank=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    batch = models.ForeignKey(Batch, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    admission_date = models.DateField(auto_now_add=True)
    roll_number = models.CharField(max_length=20, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.student_id})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    class Meta:
        ordering = ['user__first_name']
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
