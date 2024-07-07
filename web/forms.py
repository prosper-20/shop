
from django import forms
from account.models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'phone', 'address', 'shop', 'image']

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Optionally, customize the fields or widgets here