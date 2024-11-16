from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from utils.check_token import validate_token


class AuthenticationBaseRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        primary_key = view_kwargs.get('pk')
        exclude_target_urls = [reverse('auth_me'), reverse('change_password')]
        if primary_key:
            exclude_target_urls.append(reverse('chapter_detail', kwargs={'pk': primary_key}))
            exclude_target_urls.append(reverse('juz_detail', kwargs={'pk': primary_key}))

        if request.path.startswith('/api/v1/') and request.path in exclude_target_urls:
            payload = validate_token(request.headers.get('Authorization'))

            if payload is None:
                return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
            return
        return
