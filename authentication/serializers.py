from django.contrib.auth.hashers import make_password
from rest_framework import serializers

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

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.password = make_password(validated_data.get('password'))
        return super().update(instance, validated_data)


class OTPSerializer(serializers.ModelSerializer):
    class Meta:
        model = OTP
        fields = ('id', 'otp_code', 'otp_key')


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class OTPTokenSerializer(serializers.Serializer):
    otp_token = serializers.UUIDField()


class UserLoginRequestSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)
    password = serializers.CharField(required=True)


class TokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    access_token = serializers.CharField()


class ChangePasswordRequestSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class OTPTokenWithPasswordSerializer(serializers.Serializer):
    otp_token = serializers.CharField()
    password = serializers.CharField(required=True)
