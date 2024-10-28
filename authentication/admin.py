from django.contrib import admin

from .models import User, OTP

from django.contrib.auth.hashers import make_password


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email', 'first_name')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'first_name', 'email')
    list_filter = ('rate',)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attempts')
    list_display_links = ('id', 'user')
