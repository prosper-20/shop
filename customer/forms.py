from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'approval', 'status', 'exitdate')
        labels = {
            'no': 'Customer ID',
            'business': 'Business Name',
            'email': 'Email Address',
            'nature' : 'Business Type',
            'date': 'Contract Date',
            'status': 'Account Status',
            'dob': 'Date of Birth',
            'state': 'State of Origin',
            'address': 'House Address',
            'occupation': 'Occupation',
            'exitdate': 'Exit Date',
            'approval': 'Approve',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'exitdate': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['nature'].choices = [('', 'Select')] + list(self.fields['nature'].choices)
       
       