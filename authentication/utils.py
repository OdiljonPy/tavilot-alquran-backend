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
    user = User.objects.get(phone_number=data['phone_number']).first()
    if not user:
        raise CustomApiException(ErrorCodes.INVALID_INPUT.value)
    if not check_password(data['password'], user.password):
        raise CustomApiException(ErrorCodes.INVALID_INPUT.value)
    return user


def generate_otp_code():
    first_digit = random.randint(1, 9)
    digits = [str(random.randint(0, 9)) for _ in range(4)]
    return str(first_digit) + ''.join(digits)


def check_otp(otp):
    first_otp = otp.order_by('created_at').first()

    if timezone.now() - first_otp.created_at > timedelta(minutes=1):
        otp.delete()

    if len(otp) > 3:
        return True

    return False


def phone_number_validation(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(message='Phone number is invalid.')


def otp_expiring(value):
    if timezone.now() - value > timedelta(minutes=3):
        return True


def send_telegram_otp_code(otp):
    message = """P/j: Tavilot-alquran\nPhone: {}\nOTP_code {}\nExpire after < 3 minutes >""".format(
        otp.user.phone_number, otp.otp_code)
    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))

    if status.status_code != 200:
        raise ValidationError(message='Due to some reasons SMS was not sent')
