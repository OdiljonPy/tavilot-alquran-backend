from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from utils.check_token import validate_token


class AuthenticationBaseRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exclude_target_urls = [
            reverse('register'), reverse('verify'),
            reverse('login'), reverse('reset_password'),
            reverse('send_token_password'),
            reverse('verify_with_token')]

        if request.path.startswith('/api/v1/') and request.path not in exclude_target_urls:
            payload = validate_token(request.headers.get('Authorization'))

            if payload is None:
                return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
