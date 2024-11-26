import random
import re
from datetime import timedelta

from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.utils import timezone

from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException


def user_existing(data):
    from .models import User
    user = User.objects.filter(phone_number=data.get('phone_number'), is_verified=True).first()
    if not user:
        raise CustomApiException(ErrorCodes.USER_DOES_NOT_EXIST)
    if not check_password(data['password'], user.password):
        raise CustomApiException(ErrorCodes.INCORRECT_PASSWORD)
    return user


def generate_otp_code():
    return str(random.randint(100000, 999999))


def check_otp(otp):
    first_otp = otp.first()

    if first_otp and timezone.now() - first_otp.created_at > timedelta(hours=12):
        otp.delete()

    if len(otp) > 2:
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')


def phone_number_validation(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(message='Phone number is invalid.')


def otp_expiring(value):
    if timezone.now() - value > timedelta(minutes=3):
        return True


def check_otp_attempts(otp, otp_code):
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
    return otp
