from django.http import JsonResponse
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from utils.check_token import get_rate
from tavilot.views import ChapterViewSet, JuzViewSet
from rest_framework import status


class VerseMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        primary_key = view_kwargs.get('pk')
        if not primary_key:
            return
        chapter_detail_url = reverse("chapter_detail", kwargs={'pk': primary_key})
        full_juz_detail_url = reverse("full_juz_detail", kwargs={'pk': primary_key})
        if request.path in [chapter_detail_url, full_juz_detail_url]:
            rate = get_rate(request.headers.get('Authorization'))
            if request.path == chapter_detail_url and rate == 2:
                return ChapterViewSet.as_view({'get': 'chapter_detail'})(request, *view_args, **view_kwargs)
            elif request.path == full_juz_detail_url and rate == 2:
                return JuzViewSet.as_view({'get': 'get_juz_detail_full'})(request, *view_args, **view_kwargs)
        return view_func(request, *view_args, **view_kwargs)
