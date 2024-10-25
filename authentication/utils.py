import random
import re
import requests
from datetime import timedelta
from django.conf import settings

from django.core.exceptions import ValidationError
from django.utils import timezone


def generate_otp_code():
    first_digit = random.randint(1, 9)
    digits = [str(random.randint(0, 9)) for _ in range(4)]
    return str(first_digit) + ''.join(digits)


def check_otp(otp):
    first_otp = otp.order_by('created_at').first()

    if timezone.now() - first_otp.created_at > timedelta(minutes=1):
        otp.delete()

    if len(otp) > 3:
        return False

    return True


def phone_number_validation(value):
    if not re.match(r'^\+998\d{9}$', value):
        raise ValidationError(message='Phone number is invalid.')


def otp_expiring(value):
    if timezone.now() - value > timedelta(minutes=12):
        raise ValidationError(message='OTP expired.')



def send_telegram_otp_code(otp):

    message = """P/j: Tavilot-alquran\nPhone: {}\nOTP_code {}\nExpire after < 3 minutes >""".format(otp.user.phone_number, otp.otp_code)
    status = requests.get(settings.TELEGRAM_API_URL.format(settings.BOT_TOKEN, message, settings.CHANNEL_ID))

    if status.status_code != 200:
        raise ValidationError(message='Due to some reasons SMS was not sent')