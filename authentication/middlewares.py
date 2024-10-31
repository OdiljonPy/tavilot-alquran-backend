from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin
from django.urls import reverse

from utils.check_token import validate_token


class AuthenticationBaseRedirectMiddleware(MiddlewareMixin):
    def process_request(self, request):
        exclude_target_urls = [
            reverse('chapter_detail', kwargs = {'pk': 3})]

        if not request.path.startswith('/api/v1/') and request.path in exclude_target_urls:
            payload = validate_token(request.headers.get('Authorization'))

            if payload is None:
                return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
