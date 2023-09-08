from django.contrib import admin

from .models import Profile
from .forms import ProfileForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'first_name', 'last_name', 'phone']
    form = ProfileForm
