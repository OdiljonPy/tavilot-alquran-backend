from django.utils.deprecation import MiddlewareMixin
from .models import User, OTP
from django.urls import reverse


# class RegisterMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         exclude_target_url = [reverse('register')]
#         if request.path in exclude_target_url:
#             print(request, '/' * 50)
