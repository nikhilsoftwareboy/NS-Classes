"""
Enquiries Models — Admission enquiries and contact messages for NS Classes.
"""
from django.db import models


class AdmissionEnquiry(models.Model):
    """Admission enquiry from prospective students."""
    STATUS_CHOICES = [
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('admitted', 'Admitted'),
        ('rejected', 'Rejected'),
    ]
    BOARD_CHOICES = [
        ('CBSE', 'CBSE Board'),
    ]
    CLASS_CHOICES = [(str(i), f'Class {i}') for i in range(6, 13)]

    student_name = models.CharField(max_length=100)
    parent_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    board = models.CharField(max_length=10, choices=BOARD_CHOICES)
    class_level = models.CharField(max_length=5, choices=CLASS_CHOICES, verbose_name='Class')
    interested_course = models.CharField(max_length=200, blank=True)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student_name} - {self.get_board_display()} Class {self.class_level}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Admission Enquiry'
        verbose_name_plural = 'Admission Enquiries'


class ContactMessage(models.Model):
    """Contact form messages."""
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
