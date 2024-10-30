from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from utils.check_token import get_rate
from tavilot.views import ChapterViewSet
from rest_framework import status


class VerseMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        chapter_id = view_kwargs.get('pk')
        if chapter_id is None:
            return
        target_urls = reverse(viewname="chapter_detail", kwargs={'pk': chapter_id})
        if request.path in target_urls:
            rate = get_rate(request.headers.get('Authorization'))

            if rate in [2]:
                return ChapterViewSet.as_view({'get': 'chapter_detail'})(request, *view_args, **view_kwargs)
            if rate in [1]:
                return ChapterViewSet.as_view({'get': 'chapter_detail_translated_verses'})(request, *view_args, **view_kwargs)
            return JsonResponse(data={'result': 'You do not have permission', 'ok': False}, status=status.HTTP_403_FORBIDDEN)
