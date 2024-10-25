import random
import re
from datetime import timedelta

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
