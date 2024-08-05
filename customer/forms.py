from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'status', 'data_entry_officer_note', 'nextdue') # You removed approval form the list and  exitdate
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
            'Comments (Optional)': 'data_entry_officer_note',
            'Review Comments (Optional)': 'review_officer_note',
            'Approval Comments(Optional)': 'approval_officer_note',
            # 'exitdate': 'Exit Date',
            'nextdue': 'Due Date'
            # 'approval': 'Approve',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'exitdate': forms.DateInput(attrs={'type': 'date'}),
            'nextdue': forms.DateInput(attrs={'type': 'date'}),
            'data_entry_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['nature'].choices = [('', 'Select')] + list(self.fields['nature'].choices)
        self.fields['state'].choices = [('', 'Select')] + list(self.fields['state'].choices)



class EditCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'status', 'data_entry_officer_note', 'nextdue', 'approval') # You removed approval form the list and  exitdate
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
            'Comments (Optional)': 'data_entry_officer_note',
            # 'exitdate': 'Exit Date',
            'nextdue': 'Due Date',
            'approval': 'Approve',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'exitdate': forms.DateInput(attrs={'type': 'date'}),
            'nextdue': forms.DateInput(attrs={'type': 'date'}),
            'data_entry_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }


class ReviwerEditCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'status', 'data_entry_officer_note', 'review_officer_note', 'nextdue', 'approval') # You removed approval form the list and  exitdate
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
            'Comments (Optional)': 'data_entry_officer_note',
            'Your Comments (Optional)': 'review_officer_note',
            # 'exitdate': 'Exit Date',
            'nextdue': 'Due Date',
            'approval': 'Approve',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'exitdate': forms.DateInput(attrs={'type': 'date'}),
            'nextdue': forms.DateInput(attrs={'type': 'date'}),
            'data_entry_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        'review_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }



class ApproverEditCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'status', 'data_entry_officer_note', 'review_officer_note', 'approval_officer_note', 'nextdue', 'approval') # You removed approval form the list and  exitdate
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
            'Comments (Optional)': 'data_entry_officer_note',
            'Your Comments (Optional)': 'review_officer_note',
            'Approval Comments (Optional)': 'approval_officer_note',
            # 'exitdate': 'Exit Date',
            'nextdue': 'Due Date',
            'approval': 'Approve',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'exitdate': forms.DateInput(attrs={'type': 'date'}),
            'nextdue': forms.DateInput(attrs={'type': 'date'}),
            'data_entry_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        'review_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        'approval_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }

    # def __init__(self, *args, **kwargs):
    #     super(CustomerForm, self).__init__(*args, **kwargs)
    #     self.fields['nature'].choices = [('', 'Select')] + list(self.fields['nature'].choices)
    #     self.fields['state'].choices = [('', 'Select')] + list(self.fields['state'].choices)
       
       