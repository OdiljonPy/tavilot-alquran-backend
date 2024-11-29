from django.urls import path

from .views import Transaction

urlpatterns = [
    path("", Transaction.as_view({"post":"transaction"}), name="transaction"),

]
