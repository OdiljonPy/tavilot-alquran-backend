from datetime import datetime

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException
from .models import User, OTP
from .serializers import UserSerializer, PhoneNumberSerializer, OTPSerializer, OTPTokenSerializer, \
    UserLoginRequestSerializer, TokenSerializer
from .swagger_schema.requests import OTPTokenWithPasswordSerializer
from .utils import check_otp, otp_expiring, send_telegram_otp_code, user_existing


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
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Fill all blanks.')

        otp = OTP.objects.filter(otp_key=otp_key).first()
        if otp is None:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is invalid.')

        if otp_expiring(otp.created_at):
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is expired.')

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

    @swagger_auto_schema(
        operation_summary='Login user',
        operation_description='Login user',
        request_body=UserLoginRequestSerializer,
        responses={200: TokenSerializer()},
    )
    def login(self, request):
        login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        serializer = UserLoginRequestSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message=serializer.errors)

        user = user_existing(request.data)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['rate'] = user.rate
        access_token['login_time'] = login_time
        user.login_time = login_time
        user.save(update_fields=['login_time'])
        return Response({'result': {'access_token': str(access_token), 'refresh_token': refresh_token}},
                        status=status.HTTP_200_OK)


class PasswordViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Send opt code',
        operation_description='Send opt code',
        request_body=PhoneNumberSerializer,
        responses={200: OTPSerializer()},
    )
    def reset_password(self, request):
        data = request.data

        user = User.objects.filter(phone_number=data.get('phone_number')).first()

        if not user or not user.is_verified:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT,
                                     message='User does not exist. Go to Register page')

        otp = OTP.objects.create(user_id=user.id)
        if check_otp(OTP.objects.filter(user_id=user.id)):
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')

        otp.save()
        send_telegram_otp_code(otp)
        return Response({'message': {'otp_key': otp.otp_key}}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Send token for verifying password',
        operation_description='Send token for verifying password',
        request_body=OTPSerializer,
        responses={200: OTPTokenSerializer()},
        tags=['User']
    )
    def send_token_password(self, request):
        otp_key = request.data.get('otp_key', '')
        otp_code = request.data.get('otp_code', '')

        if not otp_code or not otp_key:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Fill all blanks.')

        otp = OTP.objects.filter(otp_code=otp_code).first()
        if otp_expiring(otp.created_at):
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is expired.')
        if otp.attempts > 2:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Too many attempts. Try later.')

        if otp.otp_code != otp_code:
            otp.attempts += 1
            otp.save(update_fields=['attempts'])

        return Response({'message': {'otp_token': otp.otp_token}, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Reset password with token',
        operation_description='Reset password with token',
        request_body=OTPTokenWithPasswordSerializer,
        responses={200: UserSerializer()},
    )
    def verify_with_token(self, request):
        otp_token = request.data.get('otp_token', '')
        password = request.data.get('password', '')

        if not otp_token or not password:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Fill all blanks.')
        user = User.objects.filter(otp__otp_token=otp_token).first()

        if not user:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='User does not exist.')

        serializer = UserSerializer(user, data={'password': password}, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message=serializer.errors)

        serializer.save()

        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
