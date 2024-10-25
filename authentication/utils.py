import random


def generate_otp_code():
    first_digit = random.randint(1, 9)
    digits = [str(random.randint(0, 9)) for _ in range(4)]
    return str(first_digit) + ''.join(digits)
