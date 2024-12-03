from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User, OTP
from django.utils import timezone
from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'first_name', 'last_name')
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


class RefreshTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, value):
        try:
            token = RefreshToken(value.get('refresh_token'))
        except Exception as e:
            raise serializers.ValidationError(e)
        if token.get('exp') < timezone.now().timestamp():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Refresh token expired')
        return value
