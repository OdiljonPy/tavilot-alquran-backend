from django.urls import path

from .views import TransactionViewSet, ClickTransactionViewSet

urlpatterns = [
    path("", TransactionViewSet.as_view({"post": "transaction"}), name="transaction"),

    path('click/prepare/', ClickTransactionViewSet.as_view({"post": "prepare"}), name="prepare"),
    path('click/complete/', ClickTransactionViewSet.as_view({"post": "complete"}), name="complete"),

]
