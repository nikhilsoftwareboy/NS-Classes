from django import forms
from .models import Batch
from courses.models import Course, Subject
from teachers.models import Teacher

class BatchForm(forms.ModelForm):
    class Meta:
        model = Batch
        fields = ['name', 'course', 'board', 'class_level', 'subjects', 'teacher', 'start_date', 'end_date', 'max_students', 'status']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CBSE Class 10 Morning Batch'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
            'board': forms.Select(attrs={'class': 'form-select'}),
            'class_level': forms.Select(attrs={'class': 'form-select'}),
            'subjects': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'max_students': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Capacity'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
