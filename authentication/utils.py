import random
import re
from datetime import timedelta

import requests
from django.conf import settings
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
    first_otp = otp.order_by('created_at').first()

    if timezone.now() - first_otp.created_at > timedelta(hours=12):
        otp.delete()

    if len(otp) > 3:
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='To many attempts! Try later.')


def phone_number_validation(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(message='Phone number is invalid.')


def otp_expiring(value):
    if timezone.now() - value > timedelta(minutes=3):
        return True


def send_telegram_otp_code(otp):

    message = """P/j: Tavilot-alquran\nPhone: {}\nOTP_code {}\nExpire in {}""".format(
        otp.user.phone_number, otp.otp_code, (otp.created_at + timedelta(minutes=3)).strftime('%H:%M:%S'))

    requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))


def check_otp_attempts(otp, otp_code):
    if otp is None:
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is invalid.')

    if otp_expiring(otp.created_at):
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP is expired.')

    if otp.first().attempts > 2:
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='Too many attempts.')

    if otp.otp_code != otp_code:
        otp.attempts += 1
        otp.save(update_fields=['attempts'])
        raise CustomApiException(error_code=ErrorCodes.INVALID_INPUT, message='OTP code is incorrect.')
    return otp
