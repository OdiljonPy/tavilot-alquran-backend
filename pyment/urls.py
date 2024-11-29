from django.urls import path

from .views import TransactionViewSet

urlpatterns = [
    path("", TransactionViewSet.as_view({"post":"transaction"}), name="transaction"),

]
