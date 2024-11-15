from django.urls import path

from .views import UserViewSet, PasswordViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'post': 'register'}), name='register'),
    path('me/', UserViewSet.as_view({'get': 'auth_me'}), name='auth_me'), #need to login for use
    path('verify/', UserViewSet.as_view({'post': 'verify'}), name='verify'),
    path('login/', UserViewSet.as_view({'post': 'login'}), name='login'),
    path('password/reset/', PasswordViewSet.as_view({'post': 'reset_password'}), name='reset_password'),
    path('password/send/token/', PasswordViewSet.as_view({'post': 'send_token_password'}), name='send_token_password'),
    path('password/verify/token/', PasswordViewSet.as_view({'post': 'verify_with_token'}), name='verify_with_token'),
    path('password/change/', PasswordViewSet.as_view({'post': 'change_password'}), name='change_password'),
]
