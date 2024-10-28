from django.urls import path
from .views import ChapterViewSet, VerseViewSet, PostViewSet, CategoryViewSet

urlpatterns = [
    path('chapters/', ChapterViewSet.as_view({'get': 'chapter_list'}), name='chapters'),
    path('chapters/<int:pk>/', VerseViewSet.as_view({'get': 'verse_list'}), name='verses'),
    path('verses/<int:pk>/', VerseViewSet.as_view({'get': 'verse_detail'}), name='verse_detail'),
    path('categories/', CategoryViewSet.as_view({'get': 'category_list'}), name='categories'),
    path('posts/<int:pk>/', PostViewSet.as_view({'get': 'posts_list'}), name='posts'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'post_detail'}), name='post_detail'),
]
