from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import User, OTP, ResetToken

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'first_name', 'is_verified', 'rate')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'first_name')
    list_filter = ('rate', 'is_verified')

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        if password and not change or form.initial['password'] != password:
            obj.password = make_password(password)
        return super().save_model(request, obj, form, change)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attempts')
    list_display_links = ('id', 'user')
    readonly_fields = ('user', 'attempts', 'otp_code', 'otp_key')

@admin.register(ResetToken)
class ResetTokenAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'token')
    list_display_links = ('id', 'user')
    readonly_fields = ('user', 'token')
