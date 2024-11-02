from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from utils.check_token import validate_token


class AuthenticationBaseRedirectMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        chapter_id = view_kwargs.get('pk')
        exclude_target_urls = [reverse('auth_me'), reverse('change_password')]
        if chapter_id:
            exclude_target_urls.append(reverse('chapter_detail', kwargs={'pk': chapter_id}))

        if request.path.startswith('/api/v1/') and request.path in exclude_target_urls:
            payload = validate_token(request.headers.get('Authorization'))

            if payload is None:
                return JsonResponse(data={'result': "", "error": "Unauthorized access", 'ok': False}, status=401)
            return view_func(request, *view_args, **view_kwargs)

        return None
