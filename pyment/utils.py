from hashlib import md5
from django.conf import settings
from .exception import PaymeCustomApiException, PaymeErrorCodes
from datetime import datetime, timezone
from .exception import (
    ClickPrepareException, ClickPrepareCode,
    ClickCompleteException
)


def check_amount(amount):
    if settings.SUBSCRIPTION_PRICE_PAYME != amount:
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
        raise PaymeCustomApiException(PaymeErrorCodes.INVALID_AMOUNT)

    # Check and convert 'to_millis'
    if isinstance(to_millis, (int, str)) and str(to_millis).isdigit():
        to_millis = int(to_millis)
        to = datetime.fromtimestamp(to_millis / 1000, tz=timezone.utc)
    else:
        return {"error": "'to_' value must be a valid millisecond timestamp."}

    return {"from_": from_, "to": to}


def encrypt(data):
    data_encode = md5(data.encode()).hexdigest()
    return data_encode


def check_sign_string(click_trans_id, merchant_trans_id, amount, action, sign_time, sign_string):
    payload = (f'{click_trans_id}{settings.SERVICE_ID}{settings.CLICK_SECRET_KEY}{merchant_trans_id}{amount}'
               f'{action}{sign_time}')
    encoded_payload = encrypt(payload)
    return encoded_payload == sign_string


def check_sign_string_complete(
        click_trans_id, merchant_trans_id, amount, action, sign_time, sign_string, merchant_prepare_id):
    payload = (f'{click_trans_id}{settings.SERVICE_ID}{settings.CLICK_SECRET_KEY}{merchant_trans_id}'
               f'{merchant_prepare_id}{amount}{action}{sign_time}')
    encoded_payload = encrypt(payload)
    return encoded_payload == sign_string


def validate_click_data(data):
    print('* ' * 55)
    print('data', data)
    from authentication.models import User
    from .serializers import PrepareSerializer, CompleteSerializer
    from .models import Payment

    if int(data.get('action')) not in (0, 1):
        print('* ' * 55)
        print('Action must be either 1 or 2')
        raise ClickPrepareException(
            enum_code=ClickPrepareCode.ActionNotFound,
            click_trans_id=int(data.get('click_trans_id')),
            merchant_trans_id=str(data.get('merchant_trans_id')),
            merchant_prepare_id=0
        )

    if int(data.get('action')) == 0:
        serializer = PrepareSerializer(data=data)
        if not serializer.is_valid():
            print('* ' * 55)
            print('PrepareSerializer Error', serializer.errors)
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.ClickRequestError,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=0
            )
        prepare = serializer.save()
        user = User.objects.filter(id=data.get('merchant_trans_id'), is_verified=True).first()
        if int(data.get('error')) != 0:
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.TransactionError,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=prepare.id
            )
        if int(data.get('amount')) != settings.SUBSCRIPTION_PRICE_CLICK:
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.IncorrectParameterAmount,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=prepare.id
            )
        if not user:
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.UserNotFound,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=prepare.id
            )
        if user and user.rate == 2:
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.AlreadyPaidError,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=prepare.id
            )
        if not check_sign_string(
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                amount=data.get('amount'),
                action=data.get('action'),
                sign_time=data.get('sign_time'),
                sign_string=data.get('sign_string')):
            print('* ' * 55)
            print('Error check_sign_string')
            raise ClickPrepareException(
                enum_code=ClickPrepareCode.SignCheckFailedError,
                click_trans_id=int(data.get('click_trans_id')),
                merchant_trans_id=str(data.get('merchant_trans_id')),
                merchant_prepare_id=prepare.id
            )
        payment = Payment.objects.create(click_trans_id=int(data.get('click_trans_id')), prepare_id=prepare.id)
        payment.save()
        return prepare.id

    serializer = CompleteSerializer(data=data)
    if not serializer.is_valid():
        print('* ' * 55)
        print('CompleteSerializer Error', serializer.errors)
        raise ClickCompleteException(
            enum_code=ClickPrepareCode.ClickRequestError,
            click_trans_id=int(data.get('click_trans_id')),
            merchant_trans_id=str(data.get('merchant_trans_id')),
            merchant_confirm_id=0
        )
    complete = serializer.save()
    if not check_sign_string_complete(
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
            amount=data.get('amount'),
            action=data.get('action'),
            sign_time=data.get('sign_time'),
            sign_string=data.get('sign_string'),
            merchant_prepare_id=data.get('merchant_prepare_id')):
        print('* ' * 55)
        print('Error check_sign_string_complete')
        raise ClickCompleteException(
            enum_code=ClickPrepareCode.SignCheckFailedError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
            merchant_confirm_id=complete.id
        )
    payment = Payment.objects.filter(click_trans_id=data.get('click_trans_id'), status=0).first()
    if not payment:
        raise ClickCompleteException(
            enum_code=ClickPrepareCode.TransactionNotExist,
            click_trans_id=int(data.get('click_trans_id')),
            merchant_trans_id=str(data.get('merchant_trans_id')),
            merchant_confirm_id=complete.id
        )
    payment.complete_id = complete.id
    payment.status = 1
    payment.save(update_fields=['complete_id', 'status'])
    return complete.id
