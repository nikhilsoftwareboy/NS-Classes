from django import forms
from .models import Attendance
from batches.models import Batch

class AttendanceDateSelectForm(forms.Form):
    batch = forms.ModelChoiceField(
        queryset=Batch.objects.filter(status='active'),
        widget=forms.Select(attrs={'class': 'form-select', 'onchange': 'this.form.submit()'})
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'onchange': 'this.form.submit()'})
    )
