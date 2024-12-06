from django.contrib.auth.hashers import check_password
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException
from pyment.models import Subscription
from utils.send_message import send_telegram_otp_code
from .models import User, OTP, ResetToken
from .serializers import (
    UserSerializer, PhoneNumberSerializer,
    OTPSerializer, OTPTokenSerializer,
    UserLoginRequestSerializer, TokenSerializer,
    ChangePasswordRequestSerializer,
    OTPTokenWithPasswordSerializer,
    RefreshTokenSerializer)
from .utils import check_otp, user_existing, check_otp_attempts
from django.conf import settings


class UserViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='User auth me api',
        operation_description="User authme api",
        responses={200: UserSerializer()},
        tags=['User']
    )
    def auth_me(self, request):
        user = User.objects.filter(id=request.user.id).first()
        if not user:
            raise CustomApiException(error_code=ErrorCodes.NOT_FOUND)

        serializer = UserSerializer(user, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Check user subscription',
        responses={200: "{result: True/False, prays:0}"},
        tags=['User']
    )
    def subscription_check(self, request):
        user_id = request.user.id
        return Response({"result": User.objects.filter(id=request.user.id, rate=2).exists(),
                         'user_id': user_id, 'ok': True,
                         'prays_click': settings.SUBSCRIPTION_PRICE_CLICK,
                         'prays_payme': settings.SUBSCRIPTION_PRICE_PAYME},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Registration a user api',
        operation_description='Registration a user api',
        request_body=UserSerializer,
        responses={201: UserSerializer()},
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

        check_otp(OTP.objects.filter(user_id=validated_user.id).order_by('created_at'))
        obj = OTP.objects.create(user_id=validated_user.id)

        obj.save()
        send_telegram_otp_code(obj)
        return Response(data={'result': {'otp_key': obj.otp_key}, 'ok': True},
                        status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Verify a user api',
        operation_description='Verify a user api',
        request_body=OTPSerializer,
        responses={200: OTPSerializer()},
        tags=['User']
    )
    def verify(self, request):
        serializer = OTPSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED)

        otp = check_otp_attempts(OTP.objects.filter(otp_key=serializer.validated_data.get('otp_key')).first(),
                                 serializer.validated_data.get('otp_code'))

        user = otp.user
        user.is_verified = True
        user.save(update_fields=['is_verified'])

        OTP.objects.filter(user_id=user.id).delete()
        return Response({'result': 'Successfully verified.', 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Login user api',
        operation_description='Login user api',
        request_body=UserLoginRequestSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def login(self, request):
        login_time = timezone.now().isoformat()
        serializer = UserLoginRequestSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        user = user_existing(request.data)
        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token
        access_token['rate'] = user.rate
        access_token['login_time'] = login_time
        user.login_time = login_time
        user.save()
        return Response(
            {'result': {'access_token': str(access_token), 'refresh_token': str(refresh_token),
                        'user_rate': user.rate}, 'ok': True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary='Token refresh api',
        operation_description='Token refresh api',
        request_body=RefreshTokenSerializer,
        responses={200: TokenSerializer()},
        tags=['User']
    )
    def refresh_token(self, request):
        login_time = timezone.now().isoformat()
        serializer = RefreshTokenSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message=serializer.errors)
        refresh = RefreshToken(serializer.validated_data.get('refresh_token'))
        user_id = refresh.payload.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise CustomApiException(ErrorCodes.NOT_FOUND, message='User not found')
        new_refresh_token = RefreshToken.for_user(user)
        new_access_token = new_refresh_token.access_token
        new_access_token['rate'] = user.rate
        new_access_token['login_time'] = login_time
        user.login_time = login_time
        user.save()
        return Response({'result': {'access_token': str(new_access_token), 'refresh_token': str(new_refresh_token)},
                         'ok': True}, status=status.HTTP_200_OK)


class PasswordViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='Send opt code api',
        operation_description='Send opt code api',
        request_body=PhoneNumberSerializer,
        responses={200: OTPSerializer()},
        tags=['User']
    )
    def reset_password(self, request):

        serializer = PhoneNumberSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        user = User.objects.filter(phone_number=serializer.validated_data.get('phone_number')).first()

        if not user or not user.is_verified:
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT,
                                     message='User does not exist. Go to Register page')

        if check_otp(OTP.objects.filter(user_id=user.id)):
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')

        otp = OTP.objects.create(user_id=user.id)
        otp.save()
        send_telegram_otp_code(otp)
        return Response({'result': {'otp_key': otp.otp_key}, 'ok': True}, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_summary='Send token for verifying password api',
        operation_description='Send token for verifying password api',
        request_body=OTPSerializer,
        responses={200: OTPTokenSerializer()},
        tags=['User']
    )
    def send_token_password(self, request):

        serializer = OTPSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        otp = check_otp_attempts(OTP.objects.filter(otp_key=serializer.validated_data.get('otp_key')).first(),
                                 serializer.validated_data.get('otp_code'))

        token = ResetToken.objects.create(user_id=otp.user.id)

        OTP.objects.filter(user_id=otp.user.id).delete()

        return Response(data={'result': {'token': token.token}, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Reset password with token api',
        operation_description='Reset password with token api',
        request_body=OTPTokenWithPasswordSerializer,
        responses={200: UserSerializer()},
        tags=['User']
    )
    def verify_with_token(self, request):

        serializer = OTPTokenWithPasswordSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message=serializer.errors)

        user = User.objects.filter(resettoken__token=serializer.validated_data.get('otp_token')).first()

        if not user:
            raise CustomApiException(error_code=ErrorCodes.USER_DOES_NOT_EXIST, message='User does not exist.')

        serializer = UserSerializer(user, data={'password': request.data.get('password')}, partial=True)
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        serializer.save()

        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Change password api',
        operation_description='Change password api',
        request_body=ChangePasswordRequestSerializer,
        responses={200: 'success'},
        tags=['User']
    )
    def change_password(self, request):
        serializer = ChangePasswordRequestSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=serializer.errors)

        user = User.objects.filter(id=request.user.id).first()

        if not check_password(serializer.validated_data.get('old_password'), user.password):
            raise CustomApiException(error_code=ErrorCodes.INCORRECT_PASSWORD)

        validate_data = UserSerializer(user, data={'password': serializer.validated_data.get('new_password')},
                                       partial=True)
        if not validate_data.is_valid():
            raise CustomApiException(error_code=ErrorCodes.VALIDATION_FAILED, message=validate_data.errors)
        validate_data.save()
        ResetToken.objects.filter(user_id=user.id).delete()

        return Response({'result': validate_data.data, 'ok': True}, status=status.HTTP_200_OK)
