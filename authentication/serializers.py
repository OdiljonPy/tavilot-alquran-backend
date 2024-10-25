from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from authentication.models import User, OTP


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self, **kwargs):
        self.validated_data['password'] = make_password(self.validated_data['password'])
        return super().save(**kwargs)

class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('id', 'otp_code', 'otp_key')