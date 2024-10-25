from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .models import User, OTP
from .serializers import UserSerializer


class UserViewSet(ViewSet):

    def register(self, request):
        data = request.data
        user = User.objects.filter(username=data['username'])
        if user.first() and user.is_verified:
            return Response(data={'message': 'User already exists.', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=data, partial=True) if user.exists() else UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(data={'message': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        validated_user = serializer.save()
        print(validated_user)
        obj = OTP.objects.create(user_id=validated_user.id)
        return Response(data={'message': {'otp_key': obj.otp_key}, 'otp_code': obj.otp_code},
                        status=status.HTTP_201_CREATED)
