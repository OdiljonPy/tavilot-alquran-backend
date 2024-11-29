from rest_framework import serializers
# from .models import CreateTransaction, Subscription
from django.conf import settings
from datetime import datetime, timezone
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import serializers
from .exception import PaymeErrorCodes, PaymeCustomApiException
from authentication.models import User


class AccountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        # `value` is the actual user_id, so no need to call `.get()`
        user_id = value
        if not user_id:
            raise PaymeCustomApiException(PaymeErrorCodes.INSUFFICIENT_METHOD)
        if not User.objects.filter(id=user_id, is_verified=True).exists():
            raise PaymeCustomApiException(PaymeErrorCodes.USER_NOT_FOUND)
        return value


class ParamsSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.DateTimeField()
    amount = serializers.IntegerField(min_value=100)
    account = AccountSerializer()

    def to_internal_value(self, data):
        """
        JSON ichidagi `time` millisekund qiymatini `datetime` formatiga aylantirish
        """
        time_in_millis = data.get('time')
        if isinstance(time_in_millis, str) and time_in_millis.isdigit():
            time_in_millis = int(time_in_millis)  # Millisekund qiymatini butun songa aylantirish
        if isinstance(time_in_millis, int):
            # Millisekundni `datetime` formatiga aylantirish
            data['time'] = datetime.fromtimestamp(time_in_millis / 1000, tz=timezone.utc)
        elif isinstance(time_in_millis, str):
            raise serializers.ValidationError(
                {"time": "Invalid time format. Expected millisecond timestamp as an integer."}
            )
        return super().to_internal_value(data)


class CheckPerformTransactionParamsSerializer(serializers.Serializer):
    amount = serializers.IntegerField(min_value=100)
    account = AccountSerializer()


class CheckPerformTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    params = CheckPerformTransactionParamsSerializer()

    def validate(self, data):
        # Check if 'params' contains 'account' and if 'user_id' is present within 'account'
        account = data.get('params', {}).get('account', {})
        if not account.get('user_id'):
            raise PaymeCustomApiException(PaymeErrorCodes.INSUFFICIENT_METHOD)
        return data


class CreateTransactionSerializer(serializers.Serializer):
    params = ParamsSerializer()


class CreateTransactionResponseSerializer(serializers.Serializer):
    transaction = serializers.CharField()
    state = serializers.IntegerField()
    create_time = serializers.DateTimeField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # `create_time`ni millisekundga aylantirish
        if 'create_time' in ret and isinstance(ret['create_time'], str):
            dt = datetime.fromisoformat(ret['create_time'].replace('Z', '+00:00'))
            ret['create_time'] = int(dt.timestamp() * 1000)
        return ret


class PerformTransactionParamsSerializer(serializers.Serializer):
    id = serializers.CharField()


class PerformTransactionSerializer(serializers.Serializer):
    method = serializers.CharField()
    params = PerformTransactionParamsSerializer()


class PerformTransactionResponseSerializer(serializers.Serializer):
    transaction = serializers.CharField()
    perform_time = serializers.DateTimeField()
    state = serializers.IntegerField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # `create_time`ni millisekundga aylantirish
        if 'perform_time' in ret and isinstance(ret['perform_time'], str):
            dt = datetime.fromisoformat(ret['perform_time'].replace('Z', '+00:00'))
            ret['perform_time'] = int(dt.timestamp() * 1000)
        return ret


class CheckTransactionSerializer(serializers.Serializer):
    create_time = serializers.DateTimeField()
    perform_time = serializers.DateTimeField(allow_null=True)
    cancel_time = serializers.IntegerField(default=0)
    transaction = serializers.CharField()
    state = serializers.IntegerField()
    reason = serializers.CharField(allow_null=True)

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # `create_time`ni millisekundga aylantirish
        if 'perform_time' in ret and isinstance(ret['perform_time'], str):
            dt = datetime.fromisoformat(ret['perform_time'].replace('Z', '+00:00'))
            ret['perform_time'] = int(dt.timestamp() * 1000)
        if not ret.get("perform_time"):
            ret['perform_time'] = 0
        if 'create_time' in ret and isinstance(ret['create_time'], str):
            dt = datetime.fromisoformat(ret['create_time'].replace('Z', '+00:00'))
            ret['create_time'] = int(dt.timestamp() * 1000)
        return ret


class CancelTransactionParams(serializers.Serializer):
    id = serializers.CharField()
    reason = serializers.IntegerField()


class CancelTransactionSerializer(serializers.Serializer):
    params = CancelTransactionParams()


class CancelTransactionSerializerResponse(serializers.Serializer):
    transaction = serializers.CharField()
    cancel_time = serializers.DateTimeField()
    state = serializers.IntegerField()

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        # `create_time`ni millisekundga aylantirish
        if 'cancel_time' in ret and isinstance(ret['cancel_time'], str):
            dt = datetime.fromisoformat(ret['cancel_time'].replace('Z', '+00:00'))
            ret['cancel_time'] = int(dt.timestamp() * 1000)
        return ret


class GetStatementResponseSerializer(serializers.Serializer):
    id = serializers.CharField(source='payme_id')  # Use payme_id as id
    time = serializers.IntegerField()  # Millisecond timestamp
    amount = serializers.IntegerField()
    account = AccountSerializer()  # Nested serializer for account
    create_time = serializers.IntegerField()  # Millisecond timestamp
    perform_time = serializers.IntegerField()  # Millisecond timestamp
    cancel_time = serializers.IntegerField(default=0)  # Default is 0
    transaction = serializers.CharField()
    state = serializers.IntegerField(allow_null=True, required=False)
    reason = serializers.IntegerField(allow_null=True, required=False)

    def to_representation(self, instance):
        """
        Convert DateTime fields to milliseconds and handle nested fields.
        """
        representation = super().to_representation(instance)

        # Convert datetime fields to milliseconds
        representation['time'] = int(instance.time.timestamp() * 1000) if instance.time else 0
        representation['create_time'] = int(instance.created_at.timestamp() * 1000) if instance.created_at else 0
        representation['perform_time'] = int(instance.perform_time.timestamp() * 1000) if instance.perform_time else 0
        representation['cancel_time'] = int(instance.cancel_time.timestamp() * 1000) if instance.cancel_time else 0

        # Handle account nested serializer (assuming it's part of the User model or related)
        account_data = {"phone": instance.user.phone_number}  # Assuming phone is part of the User model
        representation['account'] = account_data

        return representation
