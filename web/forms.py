
from django import forms
from account.models import Profile

class ProfileEditForm(forms.ModelForm):
    is_approved = forms.BooleanField(required=False)


    class Meta:
        model = Profile
        fields = ['role', 'phone', 'address', 'shop', 'image', ]

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)
        # Optionally, customize the fields or widgets here
        if self.instance.user.is_approved:
            self.initial['is_approved'] = True
        else:
            self.initial['is_approved'] = False

    def save(self, commit=True):
        profile = super(ProfileEditForm, self).save(commit=False)
        # Update the related CustomUser instance's is_approved field
        profile.user.is_approved = self.cleaned_data['is_approved']
        if commit:
            profile.user.save()
            profile.save()
        return profile