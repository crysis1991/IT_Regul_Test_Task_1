from django import forms
from .models import Profile, Service, SubService


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('user_id', 'first_name', 'last_name', 'phone')
        widgets = {
            'first_name': forms.TextInput,
            'last_name': forms.TextInput,
            'phone': forms.TextInput
        }


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('page', 'title', 'description')
        widgets = {
            'title': forms.TextInput,
            'description': forms.TextInput
        }


class SubServiceForm(forms.ModelForm):
    class Meta:
        model = SubService
        fields = ('page', 'title', 'description', 'service')
        widgets = {
            'title': forms.TextInput,
            'description': forms.TextInput
        }
#
#
# class TimeSlotForm(forms.ModelForm):
#     class Meta:
#         model = TimeSlot
#         fields = ('time', 'sub_service')
#         widgets = {
#             'time': forms.TimeField,
#         }
