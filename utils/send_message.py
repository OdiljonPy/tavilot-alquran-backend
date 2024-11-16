import requests
from django.conf import settings
from datetime import timedelta


def send_telegram_otp_code(otp):
    message = """P/j: Tavilot-alquran\nPhone: {}\nOTP_code {}\nExpire in {}""".format(
        otp.user.phone_number, otp.otp_code, (otp.created_at + timedelta(minutes=3)).strftime('%H:%M:%S'))

    requests.get(settings.TELEGRAM_API_URL.format(settings.TELEGRAM_BOT_TOKEN, message, settings.TELEGRAM_CHANNEL_ID))
