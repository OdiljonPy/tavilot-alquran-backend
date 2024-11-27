from django.conf import settings
from django.db.models import Prefetch
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from authentication.models import User
from exception.error_message import ErrorCodes
from exception.exceptions import CustomApiException
from .models import Subscription, CreateTransaction
from .serializers import CreateTransactionSerializer, CreateTransactionResponseSerializer, PerformTransactionSerializer, \
    PerformTransactionResponseSerializer, CheckPerformTransactionSerializer


class Transaction(ViewSet):
    def transaction(self, request):
        data = request.data
        method = data.get('method', '')
        if method == "CheckPerformTransaction":
            return self.check_perform(request)
        elif method == "CreateTransaction":
            return self.create_transaction(request)
        elif method == "PerformTransaction":
            return self.perform_transaction(request)
        raise CustomApiException(ErrorCodes.NOT_FOUND)

    @swagger_auto_schema(
        request_body=CheckPerformTransactionSerializer,
        responses={200: "result:{'allow':True}"}
    )
    def check_perform(self, request):
        serializer = CheckPerformTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": {"code": -32700, 'message': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)

        if request.data['params']['amount'] != settings.SUBSCRIPTION_PRICE:
            return Response({"error": {"code": -31001, 'message': 'Subscription price sent incorrectly'}},
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['params']['account']['user_id']

        # faqat aktiv bo‘lgan subscriptionlarni olish
        subscriptions_qs = Subscription.objects.filter(status=2)

        # Userni olish va uning active subscriptionsini prefetch qilish
        user = User.objects.filter(pk=user_id).prefetch_related(
            Prefetch('subscription', queryset=subscriptions_qs, to_attr='active_subscriptions')
        ).first()

        if not user:
            return Response({"error": {"code": -31050, 'message': "User not found"}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Agar userda active subscription mavjud bo'lsa, qayta obuna qilishni bloklash
        if user.active_subscriptions:
            return Response({"error": {"code": -31050, 'message': "You are already subscribed."}},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'result': {"allow": True}, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CreateTransactionSerializer,
        responses={200: CreateTransactionResponseSerializer()},
        tags=['Transaction'],
    )
    def create_transaction(self, request):
        # Serializerdan foydalangan holda validatsiya
        serializer = CreateTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": {"code": -32700, 'message': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)
        if request.data['params']['amount'] != settings.SUBSCRIPTION_PRICE:
            return Response({"error": {"code": -31001, 'message': 'Subscription price sent incorrectly'}},
                            status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['params']['account']['user_id']

        # faqat aktiv bo‘lgan subscriptionlarni olish
        subscriptions_qs = Subscription.objects.filter(status=2)

        # Userni olish va uning active subscriptionsini prefetch qilish
        user = User.objects.filter(pk=user_id).prefetch_related(
            Prefetch('subscription', queryset=subscriptions_qs, to_attr='active_subscriptions')
        ).first()

        if not user:
            return Response({"error": {"code": -31050, 'message': "User not found"}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Agar userda active subscription mavjud bo'lsa, qayta obuna qilishni bloklash
        if user.active_subscriptions:
            return Response({"error": {"code": -31050, 'message': "You are already subscribed."}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Subscription yaratish
        subscription = Subscription.objects.create(
            user_id=user_id,
            status=1,  # Yangi obuna holati
            amount=serializer.validated_data['params']['amount'],
            pyment_date=timezone.now()
        )

        # Transaction yaratish
        transaction_data = CreateTransaction.objects.create(
            user_id=user_id,
            amount=serializer.validated_data['params']['amount'],
            payme_id=serializer.validated_data['params']['id'],
            transaction=subscription,  # To'g'ri bog'lanish
            state=1,
            time=serializer.validated_data['params']['time']
        )

        # Response qaytarish
        response_data = {
            "result": CreateTransactionResponseSerializer({
                "transaction": subscription.id,
                "create_time": transaction_data.created_at,
                "state": transaction_data.state
            }).data,
            "ok": True
        }

        return Response(response_data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=PerformTransactionSerializer,
        responses={200: PerformTransactionResponseSerializer()},
        tags=['Transaction'],
    )
    def perform_transaction(self, request):
        # Serializerdan foydalangan holda validatsiya
        serializer = PerformTransactionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({"error": {"code": -32700, 'message': serializer.errors}},
                            status=status.HTTP_400_BAD_REQUEST)

        # `params`dagi `id`ni olishda `get()` metodidan foydalanish
        transaction_id = serializer.validated_data.get('params', {}).get('id')
        if not transaction_id:
            return Response({"error": {"code": -32700, 'message': 'Transaction ID is missing.'}},
                            status=status.HTTP_400_BAD_REQUEST)
        # Transactionni topish
        transaction_data = CreateTransaction.objects.filter(
            payme_id=transaction_id,
        ).first()

        if not transaction_data:
            return Response({"error": {"code": -31003, 'message': 'Transaction does not exist.'}},
                            status=status.HTTP_400_BAD_REQUEST)

        if transaction_data and transaction_data.state != 1:
            return Response({"error": {"code": -31003, 'message': 'Transaction state is invalid.'}},
                            status=status.HTTP_400_BAD_REQUEST)

        # Transactionni yangilash
        transaction_data.state = 2
        transaction_data.save()

        # Transactionning bog'liq obyektini yangilash
        transaction_data.transaction.status = 2
        transaction_data.transaction.pyment_date = timezone.now()
        transaction_data.transaction.save(update_fields=['status', 'pyment_date'])
        transaction_data.user.rate = 2
        transaction_data.user.login_time = timezone.now()
        transaction_data.user.save(update_fields=['rate', 'login_time'])

        # Response qaytarish
        response_data = {
            "result": PerformTransactionResponseSerializer({
                "transaction": transaction_data.id,
                "perform_time": transaction_data.created_at,
                "state": 2
            }).data,
            "ok": True
        }
        return Response(response_data, status=status.HTTP_200_OK)
