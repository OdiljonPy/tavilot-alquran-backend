from django.contrib import admin

from .models import User, OTP

from django.contrib.auth.hashers import make_password


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone_number', 'email', 'first_name')
    list_display_links = ('id', 'phone_number')
    search_fields = ('phone_number', 'first_name', 'email')
    list_filter = ('rate',)

    def save_model(self, request, obj, form, change):
        password = form.cleaned_data.get('password')
        print(password, '/' * 50)
        if password and not change or form.initial['password'] != password:
            obj.password = make_password(password)
        super().save_model(request, obj, form, change)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'attempts')
    list_display_links = ('id', 'user')
