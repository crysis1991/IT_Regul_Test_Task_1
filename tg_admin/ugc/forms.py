from django import forms
from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'phone')
        widgets = {
            'first_name': forms.TextInput,
            'last_name': forms.TextInput,
            'phone': forms.TextInput
        }
