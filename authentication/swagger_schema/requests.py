from rest_framework import serializers

class OTPTokenWithPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    otp_token = serializers.UUIDField()