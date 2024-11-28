from rest_framework import serializers
from .models import CreateTransaction, Subscription
from django.conf import settings
from datetime import datetime, timezone
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class ParamsSerializer(serializers.Serializer):
    id = serializers.CharField()
    time = serializers.DateTimeField()
    amount = serializers.IntegerField(min_value=2000)
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
    amount = serializers.IntegerField(min_value=2000)
    account = AccountSerializer()


class CheckPerformTransactionSerializer(serializers.Serializer):
    id = serializers.CharField()
    params = CheckPerformTransactionParamsSerializer()


class CreateTransactionSerializer(serializers.Serializer):
    method = serializers.CharField()
    params = ParamsSerializer()

    def validate_method(self, value):
        if value != "CreateTransaction":
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message="Method must be 'CreateTransaction'")
        return value


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
