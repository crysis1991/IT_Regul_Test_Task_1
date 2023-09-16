from django.contrib import admin
from django.http import HttpRequest
from .models import Profile, Service, SubService, Date, TimeSlot, Order
from .forms import ProfileForm, ServiceForm, SubServiceForm


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'first_name', 'last_name', 'phone']
    form = ProfileForm


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'description']
    form = ServiceForm


@admin.register(SubService)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['page', 'title', 'description', 'service', 'price']
    form = SubServiceForm


@admin.register(Date)
class DateAdmin(admin.ModelAdmin):
    list_display = ['date']


@admin.register(TimeSlot)
class TimeAdmin(admin.ModelAdmin):
    list_display = ['time']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'user_verbose', 'service_verbose', 'date_verbose', 'time_verbose']

    def user_verbose(self, obj: Order) -> str:
        return f'{obj.user.first_name} {obj.user.last_name}'

    def service_verbose(self, obj: Order) -> str:
        return obj.service.title

    def date_verbose(self, obj: Order) -> str:
        return obj.date.date

    def time_verbose(self, obj: Order) -> str:
        return obj.time.time

