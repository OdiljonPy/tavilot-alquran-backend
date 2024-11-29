from django.conf import settings
from .exception import PaymeCustomApiException, PaymeErrorCodes
from datetime import datetime, timezone


def check_amount(amount):
    if settings.SUBSCRIPTION_PRICE != amount:
        raise PaymeCustomApiException(PaymeErrorCodes.INVALID_AMOUNT)
    return


def convert_timestamps(from_millis, to_millis):
    """
    Convert millisecond timestamps to datetime objects.

    Args:
        from_millis (int/str): Millisecond timestamp for 'from_'.
        to_millis (int/str): Millisecond timestamp for 'to_'.

    Returns:
        dict: Dictionary containing 'from_' and 'to' as datetime objects or error message.
    """
    # Check and convert 'from_millis'
    if isinstance(from_millis, (int, str)) and str(from_millis).isdigit():
        from_millis = int(from_millis)
        from_ = datetime.fromtimestamp(from_millis / 1000, tz=timezone.utc)
    else:
        return {"error": "'from_' value must be a valid millisecond timestamp."}

    # Check and convert 'to_millis'
    if isinstance(to_millis, (int, str)) and str(to_millis).isdigit():
        to_millis = int(to_millis)
        to = datetime.fromtimestamp(to_millis / 1000, tz=timezone.utc)
    else:
        return {"error": "'to_' value must be a valid millisecond timestamp."}

    return {"from_": from_, "to": to}
