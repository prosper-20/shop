from django import forms
from .models import Customer

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'title', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', "other_state", 'status', 'data_entry_officer_note', 'nextdue') # You removed approval form the list and  exitdate
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

    other_state = forms.CharField(max_length=225, required=False, widget=forms.TextInput(attrs={'placeholder': 'Specify state'}))
    outstanding_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['nature'].choices = sorted(Customer.NATURE, key=lambda x: x[1])
        # self.fields['nature'].choices = [('', 'Select')] + list(self.fields['nature'].choices)
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

    other_state = forms.CharField(max_length=225, required=False, widget=forms.TextInput(attrs={'placeholder': 'Specify state'}))
    outstanding_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field

class ReviwerEditCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'other_state', 'status', 'outstanding_balance', 'data_entry_officer_note', 'review_officer_note', 'nextdue', 'approval') # You removed approval form the list and  exitdate
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
        'review_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }

    other_state = forms.CharField(max_length=225, required=False, widget=forms.TextInput(attrs={'placeholder': 'Specify state'}))
    outstanding_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field



class ApproverEditCustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'name', 'business', 'email', 'phone', 'nature', 'occupation', 'date', 'dob', 'address', 'state', 'other_state',  'status', 'outstanding_balance', 'data_entry_officer_note', 'review_officer_note', 'approval_officer_note', 'nextdue', 'approval') # You removed approval form the list and  exitdate
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


    other_state = forms.CharField(max_length=225, required=False, widget=forms.TextInput(attrs={'placeholder': 'Specify state'}))
    outstanding_balance = forms.DecimalField(max_digits=10, decimal_places=2, required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field



    # def __init__(self, *args, **kwargs):
    #     super(CustomerForm, self).__init__(*args, **kwargs)
    #     self.fields['nature'].choices = [('', 'Select')] + list(self.fields['nature'].choices)
    #     self.fields['state'].choices = [('', 'Select')] + list(self.fields['state'].choices)
       
       