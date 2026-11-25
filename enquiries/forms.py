from django import forms
from .models import AdmissionEnquiry

class EnquiryStatusUpdateForm(forms.ModelForm):
    class Meta:
        model = AdmissionEnquiry
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
        }
