from django import forms
from .models import Customer
from django.db.models import Max

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ('no', 'title', 'name', 'business', 'email', 'phone', 'nature', 'other_business_type', 'occupation', 'date', 'dob', 'address', 'state', "other_state", 'status', 'outstanding_balance', 'data_entry_officer_note', 'nextdue') # You removed approval form the list and  exitdate
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
            'Oustanding Balance (Optional)': 'oustanding_balance',
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
            # 'oustanding_balance': forms.NumberInput(attrs={ 'placeholder': 'Enter balance here',
            # 'class': 'form-control'}),
            'data_entry_officer_note': forms.TextInput(attrs={
            'placeholder': 'Enter comment here...',
            'class': 'form-control',
            'id': 'text-field-id',
            'maxlength': '1000',  # Example: limit the length of input
        }),
        }

    other_state = forms.CharField(max_length=225, required=False, widget=forms.TextInput(attrs={'placeholder': 'Specify state'}))
    outstanding_balance = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field
    other_business_type = forms.CharField(label='Specify Business', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'other_business_type'}),
    )

    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        last_no = Customer.objects.aggregate(last_no=Max('no'))['last_no']
        if last_no:
            next_no = str(int(last_no) + 1).zfill(5)
        else:
            next_no = '10001'  # Starting number if no customers exist

        # Set the initial value for the 'no' field in the form
        self.fields['no'].initial = next_no
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
    outstanding_balance = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'placeholder': 'Outstanding Balance'}))  # Added field

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
       
       