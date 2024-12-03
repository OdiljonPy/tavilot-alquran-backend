from hashlib import md5
from django.conf import settings
from .exception import PaymeCustomApiException, PaymeErrorCodes
from datetime import datetime, timezone
from .exception import ClickCustomApiException, ClickEnumException


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
    payload = (f'{click_trans_id}{settings.SERVICE_ID}{settings.SECRET_KEY}{merchant_trans_id}{amount}'
               f'{action}{sign_time}')
    encoded_payload = encrypt(payload)
    print('* ' * 40)
    print(encoded_payload)
    return encoded_payload == sign_string


def check_sign_string_complete(
        click_trans_id, merchant_trans_id, amount, action, sign_time, sign_string, merchant_prepare_id):
    payload = (f'{click_trans_id}{settings.SERVICE_ID}{settings.SECRET_KEY}{merchant_trans_id}'
               f'{merchant_prepare_id}{amount}{action}{sign_time}')
    encoded_payload = encrypt(payload)
    print('* ' * 40)
    print(encoded_payload)
    return encoded_payload == sign_string


def validate_click_data(data):
    print(data)
    from authentication.models import User
    from .serializers import PrepareSerializer, CompleteSerializer, ClickValidateSerializer
    from .models import Payment
    serializer = ClickValidateSerializer(data=data)
    if not serializer.is_valid():
        print(serializer.errors)
        raise ClickCustomApiException(
            enum_code=ClickEnumException.ClickRequestError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    user = User.objects.filter(id=data.get('merchant_trans_id'), is_verified=True).first()
    if int(data.get('error')) != 0:
        raise ClickCustomApiException(
            enum_code=ClickEnumException.TransactionError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    if int(data.get('amount')) != settings.SUBSCRIPTION_PRICE:
        raise ClickCustomApiException(
            enum_code=ClickEnumException.IncorrectParameterAmount,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    if not user:
        raise ClickCustomApiException(
            enum_code=ClickEnumException.UserNotFound,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    if user and user.rate == 2:
        raise ClickCustomApiException(
            enum_code=ClickEnumException.AlreadyPaidError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id')
        )
    if int(data.get('action')) == 0:
        serializer = PrepareSerializer(data=data)
        if not serializer.is_valid():
            print(serializer.errors)
            raise ClickCustomApiException(
                enum_code=ClickEnumException.ClickRequestError,
                click_trans_id=data.get('click_trans_id'),
                merchant_trans_id=data.get('merchant_trans_id'),
            )
        if not check_sign_string(
                serializer.validated_data.get('click_trans_id'),
                serializer.validated_data.get('merchant_trans_id'),
                data.get('amount'),
                data.get('action'),
                serializer.validated_data.get('sign_time'),
                serializer.validated_data.get('sign_string')):
            raise ClickCustomApiException(
                enum_code=ClickEnumException.SignCheckFailedError,
                click_trans_id=data.get('click_trans_id'),
                merchant_trans_id=data.get('merchant_trans_id')
            )
        prepare = serializer.save()
        payment = Payment.objects.create(click_trans_id=data.get('click_trans_id'), prepare_id=prepare.id)
        payment.save()
        return prepare.id
    serializer = CompleteSerializer(data=data)
    if not serializer.is_valid():
        print(serializer.errors)
        raise ClickCustomApiException(
            enum_code=ClickEnumException.ClickRequestError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    if not check_sign_string_complete(
            serializer.validated_data.get('click_trans_id'),
            serializer.validated_data.get('merchant_trans_id'),
            data.get('amount'),
            data.get('action'),
            serializer.validated_data.get('sign_time'),
            serializer.validated_data.get('sign_string'),
            data.get('merchant_prepare_id')):
        print('Error')
        raise ClickCustomApiException(
            enum_code=ClickEnumException.SignCheckFailedError,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    payment = Payment.objects.filter(prepare_id=serializer.validated_data.get('merchant_prepare_id')).first()
    if not payment:
        raise ClickCustomApiException(
            enum_code=ClickEnumException.TransactionNotExist,
            click_trans_id=data.get('click_trans_id'),
            merchant_trans_id=data.get('merchant_trans_id'),
        )
    complete = serializer.save()
    payment.complete_id = complete.id
    payment.status = 1
    payment.save(update_fields=['complete_id', 'status'])
    return complete.id
