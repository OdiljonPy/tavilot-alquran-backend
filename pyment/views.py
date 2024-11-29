from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from .exception import PaymeCustomApiException, PaymeErrorCodes
from .models import Subscription, Transaction
from .serializers import (
    CreateTransactionSerializer, CreateTransactionResponseSerializer,
    PerformTransactionSerializer, PerformTransactionResponseSerializer,
    CheckPerformTransactionSerializer, CheckTransactionSerializer, CancelTransactionSerializer,
    CancelTransactionSerializerResponse, GetStatementResponseSerializer
)
from .utils import check_amount, convert_timestamps


class TransactionViewSet(ViewSet):
    def transaction(self, request):
        method = request.data.get('method')
        method_mapping = {
            "CheckPerformTransaction": self.check_perform,
            "CreateTransaction": self.create_transaction,
            "PerformTransaction": self.perform_transaction,
            "CheckTransaction": self.check_transaction,
            'CancelTransaction': self.cancel_transaction,
            "GetStatement": self.statement_transaction,
        }
        if method not in method_mapping:
            raise PaymeCustomApiException(PaymeErrorCodes.ERROR_REQUEST)
        return method_mapping[method](request)

    @swagger_auto_schema(
        request_body=CheckPerformTransactionSerializer,
        responses={200: "result:{'allow':True}"}
    )
    def check_perform(self, request):
        account = request.data.get('params', {}).get('account', {})
        if not account.get('user_id'):
            raise PaymeCustomApiException(PaymeErrorCodes.INSUFFICIENT_METHOD)
        serializer = CheckPerformTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['params']['amount']
        user_id = serializer.validated_data['params']['account']['user_id']
        check_amount(amount)
        if User.objects.filter(id=user_id, rate=2).exists():
            raise PaymeCustomApiException(PaymeErrorCodes.TRANSACTION_EXISTS)
        return Response({"jsonrpc": "2.0", 'result': {"allow": True}, 'ok': True}, status=status.HTTP_200_OK)

    def create_transaction(self, request):
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        amount = serializer.validated_data['params']['amount']
        user_id = serializer.validated_data['params']['account']['user_id']
        check_amount(amount)
        if User.objects.filter(id=user_id, rate=2).exists():
            raise PaymeCustomApiException(PaymeErrorCodes.TRANSACTION_EXISTS)
        transaction_obj = Transaction.objects.filter(payme_id=serializer.validated_data['params']['id'],
                                                     state=1).first()
        if transaction_obj and transaction_obj.payme_id == serializer.validated_data['params']['id'] and \
                datetime.now() - transaction_obj.time < timedelta(hours=12):
            return Response({
                "jsonrpc": "2.0",
                "result": CreateTransactionResponseSerializer({
                    "transaction": transaction_obj.transaction.id,
                    "create_time": transaction_obj.created_at,
                    "state": transaction_obj.state
                }).data,
                "ok": True
            }, status=status.HTTP_200_OK)
        if transaction_obj and transaction_obj.payme_id != serializer.validated_data['params']['id'] and \
                datetime.now() - transaction_obj.time < timedelta(hours=12):
            raise PaymeCustomApiException(PaymeErrorCodes.TRANSACTION_EXISTS)
        subscription = Subscription.objects.create(user_id=user_id, status=1,
                                                   amount=serializer.validated_data['params']['amount'],
                                                   pyment_date=timezone.now()
                                                   )
        transaction = Transaction.objects.create(
            user_id=user_id, amount=serializer.validated_data['params']['amount'],
            payme_id=serializer.validated_data['params']['id'], transaction=subscription, state=1,
            time=serializer.validated_data['params']['time']
        )

        return Response({
            "jsonrpc": "2.0",
            "result": CreateTransactionResponseSerializer({
                "transaction": subscription.id,
                "create_time": transaction.created_at,
                "state": transaction.state
            }).data,
            "ok": True
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PerformTransactionSerializer,
        responses={200: PerformTransactionResponseSerializer()},
        tags=['Transaction'],
    )
    def perform_transaction(self, request):
        serializer = PerformTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            raise PaymeCustomApiException(PaymeErrorCodes.OPERATION_CANNOT_PERFORMED)

        transaction = Transaction.objects.filter(
            payme_id=serializer.validated_data['params']['id']
        ).select_related('user', 'transaction').first()

        if not transaction:
            raise PaymeCustomApiException(PaymeErrorCodes.INSUFFICIENT_METHOD)

        if transaction.state == 1:
            transaction.state = 2
            transaction.perform_time = timezone.now()
            transaction.save()
            subscription = transaction.transaction
            subscription.status = 2
            subscription.pyment_date = timezone.now()
            subscription.save()
            user = transaction.user
            user.rate = 2
            user.login_time = timezone.now()
            user.save()

        return Response({
            "jsonrpc": "2.0",
            "result": PerformTransactionResponseSerializer({
                "transaction": transaction.id,
                "perform_time": transaction.perform_time,
                "state": transaction.state
            }).data,
            "ok": True
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PerformTransactionSerializer,
        responses={200: CheckTransactionSerializer()},
    )
    def check_transaction(self, request):
        serializer = PerformTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            raise PaymeCustomApiException(PaymeErrorCodes.OPERATION_CANNOT_PERFORMED)

        transaction = Transaction.objects.filter(
            payme_id=serializer.validated_data['params']['id']
        ).first()

        if not transaction:
            raise PaymeCustomApiException(PaymeErrorCodes.INSUFFICIENT_METHOD)

        response_data = CheckTransactionSerializer({
            "create_time": transaction.created_at,
            "perform_time": transaction.perform_time if transaction.state != 1 else None,
            "transaction": transaction.transaction.id,
            "state": transaction.state
        }).data

        return Response({"jsonrpc": "2.0", "result": response_data, "ok": True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CancelTransactionSerializer()
    )
    def cancel_transaction(self, request):
        serializer = CancelTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            raise PaymeCustomApiException(PaymeErrorCodes.UNABLE_CANCEL)
        transaction_obj = Transaction.objects.filter(id=serializer.validated_data['params']['id']).first()
        if not transaction_obj:
            raise PaymeCustomApiException(PaymeErrorCodes.TRANSACTION_NOT_FOUND)
        if transaction_obj.state == 1:
            transaction_obj.state = -1
        else:
            transaction_obj.state = -2
        transaction_obj.reason = serializer.validated_data['params']['reason']
        transaction_obj.cancel_time = timezone.now()
        transaction_obj.save()
        transaction_obj.user.rate = 1
        transaction_obj.user.login_time = timezone.now()
        transaction_obj.user.save()
        transaction_obj.transaction.status = 3
        transaction_obj.transaction.save()
        return Response({
            "jsonrpc": "2.0",
            "result": {CancelTransactionSerializerResponse(
                {"transaction": transaction_obj.transaction.id, 'cancel_time': transaction_obj.cancel_time,
                 'state': transaction_obj.state}).data}}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: GetStatementResponseSerializer(many=True)},
    )
    def statement_transaction(self, request):
        # Get 'from' and 'to' from request
        from_ = request.data["params"].get('from')
        to_ = request.data["params"].get('to')
        date = convert_timestamps(from_, to_)
        if not date.get('from_') or not date.get('to_'):
            return Response({"result": {'transactions': []}})
        # Filter transactions based on the given time range
        transactions = Transaction.objects.filter(created_at__gte=date.get('from_'), created_at__lte=date.get('to'), reason__isnull=True)

        # If no transactions found, return empty list
        if not transactions:
            return Response({"result": {'transactions': []}})

        # Serialize the data
        serializer = GetStatementResponseSerializer(transactions, many=True)

        # Return the response
        return Response({"result": {'transactions': serializer.data}}, status=status.HTTP_200_OK)
