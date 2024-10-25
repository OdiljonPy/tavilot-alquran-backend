from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException
from .models import User, OTP
from .serializers import UserSerializer, OTPSerializer
from .utils import check_otp, otp_expiring, send_telegram_otp_code


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Registration a user',
        operation_description='Registration a user',
        request_body=UserSerializer,
        responses={200: UserSerializer()},
        tags=['User']
    )
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
        send_telegram_otp_code(obj)
        return Response(data={'message': {'otp_key': obj.otp_key}, 'otp_code': obj.otp_code},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Verify a user',
        operation_description='Verify a user',
        request_body=OTPSerializer,
        responses={200: OTPSerializer()},
        tags=['User']
    )
    def verify(self, request):
        otp_code = request.data.get('otp_code', '')
        otp_key = request.data.get('otp_key', '')

        if not otp_code or not otp_key:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP code must be provided.')

        otp = OTP.objects.filter(otp_key=otp_key).first()
        if otp is None:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is invalid.')

        otp_expiring(otp.created_at)

        if otp.attempts > 2:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Too many attempts.')

        if otp.otp_code != otp_code:
            otp.attempts += 1
            otp.save(update_fields=['attempts'])
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP code is incorrect.')

        user = otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        OTP.objects.filter(user_id=user.id).delete()
        return Response({'message': 'Successfully verified.', 'ok': True}, status=status.HTTP_200_OK)
