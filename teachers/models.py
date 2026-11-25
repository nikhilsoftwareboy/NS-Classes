"""
Teachers Models — Teacher profiles for NS Classes.
"""
from django.db import models
from django.contrib.auth.models import User
from courses.models import Subject


class Teacher(models.Model):
    """Teacher profile linked to a Django User."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    phone = models.CharField(max_length=15)
    qualification = models.CharField(max_length=200)
    specialization = models.ManyToManyField(Subject, related_name='specialist_teachers', blank=True)
    experience = models.PositiveIntegerField(help_text='Years of experience', default=0)
    bio = models.TextField(blank=True, help_text='Short biography')
    joining_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.teacher_id})"

    @property
    def full_name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email

    class Meta:
        ordering = ['user__first_name']
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
