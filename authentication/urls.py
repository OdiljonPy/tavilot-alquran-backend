from django.urls import path

from .views import UserViewSet, PasswordViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'put': 'register'}), name='register'),
    path('verify/', UserViewSet.as_view({'put': 'verify'}), name='verify'),
    path('password/rest/', PasswordViewSet.as_view({'put': 'reset_password'}), name='reset_password'),
    path('password/send/token/', PasswordViewSet.as_view({'put': 'send_token_password'}), name='send_token_password'),
    path('password/verify/token/', PasswordViewSet.as_view({'put': 'verify_with_token'}), name='verify_with_token'),
]
