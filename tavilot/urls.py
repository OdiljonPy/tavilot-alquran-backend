from django.urls import path
from .views import ChapterViewSet, VerseViewSet

urlpatterns = [
    path('chapters/', ChapterViewSet.as_view({'get': 'chapter_list'}), name='chapters'),
    path('verses/<int:pk>/', VerseViewSet.as_view({'get': 'verse_list'}), name='verses'),
]