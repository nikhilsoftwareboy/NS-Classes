"""
Website Models — Gallery, Testimonials, FAQ for NS Classes public site.
"""
from django.db import models


class Gallery(models.Model):
    """Gallery images for the public website."""
    CATEGORY_CHOICES = [
        ('classroom', 'Classroom'),
        ('activities', 'Student Activities'),
        ('events', 'Events'),
        ('seminars', 'Seminars'),
        ('achievements', 'Achievements'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    is_active = models.BooleanField(default=True)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-upload_date']
        verbose_name = 'Gallery Image'
        verbose_name_plural = 'Gallery'


class Testimonial(models.Model):
    """Student testimonials/reviews."""
    student_name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    course_class = models.CharField(max_length=100, verbose_name='Course / Class')
    review = models.TextField()
    rating = models.PositiveIntegerField(default=5, help_text='Rating out of 5')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student_name} - {self.rating}/5"

    class Meta:
        ordering = ['-created_at']


class FAQ(models.Model):
    """Frequently asked questions."""
    question = models.CharField(max_length=300)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.question

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
