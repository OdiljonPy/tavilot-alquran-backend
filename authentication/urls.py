from django.urls import path


from .views import UserViewSet

urlpatterns = [
    path('register/', UserViewSet.as_view({'put': 'register'}), name='register'),
    path('verify/', UserViewSet.as_view({'put': 'verify'}), name='verify'),
]
