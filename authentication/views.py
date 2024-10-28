from datetime import datetime

from django.contrib.auth.hashers import check_password
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException
from .models import User, OTP
from .serializers import UserSerializer, PhoneNumberSerializer, OTPSerializer, OTPTokenSerializer, \
    UserLoginRequestSerializer, TokenSerializer, ChangePasswordRequestSerializer
from .swagger_schema.requests import OTPTokenWithPasswordSerializer
from .utils import check_otp, send_telegram_otp_code, user_existing, check_otp_attempts


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
            raise CustomApiException(error_code=ErrorCodes.USER_ALREADY_EXISTS)

        serializer = UserSerializer(user, data=data, partial=True) if user else UserSerializer(data=data)

        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED)
        validated_user = serializer.save()
        obj = OTP.objects.create(user_id=validated_user.id)
        if check_otp(OTP.objects.filter(user_id=validated_user.id)):
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')

        obj.save()
        send_telegram_otp_code(obj)
        return Response(data={'result': {'otp_key': obj.otp_key, 'otp_code': obj.otp_code}, 'ok': True},
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

        otp = check_otp_attempts(OTP.objects.filter(otp_key=otp_key).first(), otp_code)
        print(otp)

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
        user.save()
        print(user)
        return Response(
            {'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token)}, 'ok': True},
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
        return Response({'message': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

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

        otp = check_otp_attempts(OTP.objects.filter(otp_code=otp_code).first(), otp_code)

        return Response({'message': {'otp_token': otp.otp_token}, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Reset password with token',
        operation_description='Reset password with token',
        request_body=OTPTokenWithPasswordSerializer,
        responses={200: UserSerializer()},
    )
    def verify_with_token(self, request):

        serializer = OTPTokenWithPasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message=serializer.errors)

        user = User.objects.filter(otp__otp_token=request.data.get('otp_token')).first()

        if not user:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST, message='User does not exist.')

        serializer = UserSerializer(user, data={'password': request.data.get('password')}, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()
        OTP.objects.filter(user_id=user.id).delete()

        return Response(data={'message': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Change password',
        operation_description='Change password',
        request_body=ChangePasswordRequestSerializer,
        responses={200: 'success'},
    )
    def change_password(self, request):
        serializer = ChangePasswordRequestSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message=serializer.errors)
        print(request.user)

        user = User.objects.filter(id=request.user.id).first()
        print(user)
        print(user.password)
        print(request.user.password)

        if not check_password(request.data.get('old_password'), user.password):
            raise CustomApiException(error_code=ErrorCodes.INCORRECT_PASSWORD)

        validate_data = UserSerializer(user, data={'password': request.data.get('new_password')}, partial=True)
        if not validate_data.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=validate_data.errors)
        validate_data.save()

        return Response({'result': validate_data.data, 'ok': True}, status=status.HTTP_200_OK)
