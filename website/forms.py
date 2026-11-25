from django import forms
from enquiries.models import AdmissionEnquiry, ContactMessage

class PublicAdmissionForm(forms.ModelForm):
    board = forms.ChoiceField(
        choices=[('CBSE', 'CBSE Board')],
        widget=forms.Select(attrs={'class': 'form-select', 'required': True}),
        initial='CBSE'
    )
    class Meta:
        model = AdmissionEnquiry
        fields = ['student_name', 'parent_name', 'phone', 'email', 'board', 'class_level', 'interested_course', 'message']
        widgets = {
            'student_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Student's Full Name", 'required': True}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Enter Parent / Guardian's Name", 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter 10-digit Mobile Number', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address (Optional)'}),
            'board': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'class_level': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'interested_course': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. CBSE Class 10 Science, CBSE Class 12 PCM'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any specific questions or requirements...'}),
        }

class PublicContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Full Name', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email Address', 'required': True}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone Number'}),
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Message Subject', 'required': True}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'How can we help you?', 'required': True}),
        }
