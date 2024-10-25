import random
from datetime import datetime, timedelta
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
