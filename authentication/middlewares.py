from django.utils.deprecation import MiddlewareMixin
from .models import User
from django.urls import reverse


class RegisterMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exclude_target_url = [reverse('register')]
        if request.path not in exclude_target_url:
            user = User.objects.filter(username=request.user.username)
