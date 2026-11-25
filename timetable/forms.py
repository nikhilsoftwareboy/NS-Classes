from django import forms
from .models import TimetableEntry
from batches.models import Batch
from courses.models import Subject
from teachers.models import Teacher

class TimetableEntryForm(forms.ModelForm):
    class Meta:
        model = TimetableEntry
        fields = ['batch', 'day', 'subject', 'teacher', 'start_time', 'end_time', 'room']
        widgets = {
            'batch': forms.Select(attrs={'class': 'form-select'}),
            'day': forms.Select(attrs={'class': 'form-select'}),
            'subject': forms.Select(attrs={'class': 'form-select'}),
            'teacher': forms.Select(attrs={'class': 'form-select'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'room': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Room 101, Hall A'}),
        }
