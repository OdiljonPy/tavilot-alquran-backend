from django.urls import path

from .views import Transaction

urlpatterns = [
    path('create/', Transaction.as_view({"post": 'create_transaction'}), name='create'),
    path('perform/', Transaction.as_view({"post": 'perform_transaction'}), name='perform'),

]
