from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from tavilot.views import VerseViewSet


class VerseMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        target_urls = [reverse("some_name")]
        if request.path in target_urls:
            rate = get_rate(request.headers.get('Authorization'))

            if rate in [2]:
                return VerseViewSet.as_view('get': 'verse_list')(view_func, *view_args, **view_kwargs)
            if rate in [1]:
                return VerseViewSet.as_view('get': 'verse_list')(view_func, *view_args, **view_kwargs)
            return JsonResponse(data={'result': 'You do not have permission', 'ok': False}, status=status)
