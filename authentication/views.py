from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException

from .models import User, OTP
from .serializers import UserSerializer
from .utils import check_otp


class UserViewSet(ViewSet):

    def register(self, request):
        data = request.data
        user = User.objects.filter(phone_number=data.get('phone_number')).first()
        if user and user.is_verified:
            return Response(data={'message': 'User already exists.', 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user, data=data, partial=True) if user else UserSerializer(data=data)

        if not serializer.is_valid():
            return Response(data={'message': serializer.errors, 'ok': False}, status=status.HTTP_400_BAD_REQUEST)

        validated_user = serializer.save()
        obj = OTP.objects.create(user_id=validated_user.id)
        if check_otp(OTP.objects.filter(user_id=validated_user.id)) is False:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')

        obj.save()
        return Response(data={'message': {'otp_key': obj.otp_key}, 'otp_code': obj.otp_code},
                        status=status.HTTP_201_CREATED)
