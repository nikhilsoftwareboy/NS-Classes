from django import forms
from django.contrib.auth.models import User
from .models import Teacher
from courses.models import Subject

class TeacherForm(forms.ModelForm):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))
    username = forms.CharField(max_length=150, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username (Auto-generated if blank)'}))
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password (default: teacher@123)'}))

    class Meta:
        model = Teacher
        fields = [
            'teacher_id', 'photo', 'phone', 'qualification',
            'specialization', 'experience', 'bio', 'joining_date', 'is_active'
        ]
        widgets = {
            'teacher_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. NS-TCH-001'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. M.Sc. Physics, B.Ed.'}),
            'specialization': forms.SelectMultiple(attrs={'class': 'form-select'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of experience'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Brief summary or expertise'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
