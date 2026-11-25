from django import forms
from .models import FeeRecord
from students.models import Student

class FeeRecordForm(forms.ModelForm):
    class Meta:
        model = FeeRecord
        fields = ['student', 'total_fee', 'paid_amount', 'payment_date', 'payment_method', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'total_fee': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Total Course Fee'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount Paid'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Payment notes (e.g. Cheque No / UPI Ref ID)'}),
        }

class RecordPaymentForm(forms.Form):
    additional_payment = forms.DecimalField(
        max_digits=10, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount to pay now'})
    )
    payment_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    payment_method = forms.ChoiceField(
        choices=FeeRecord.PAYMENT_METHOD_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    remarks = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'UPI Ref, Cheque No, Transaction ID'})
    )
