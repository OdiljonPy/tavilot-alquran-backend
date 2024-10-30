from django.urls import path
from .views import ChapterViewSet, PostViewSet, CategoryViewSet, SheikhViewSet, AboutUsViewSet, VerseViewSet

urlpatterns = [
    path('chapters/', ChapterViewSet.as_view({'get': 'chapter_list'}), name='chapters'),
    path('chapter/<int:pk>/', ChapterViewSet.as_view({'get': 'chapter_detail'}), name='chapter_detail'),
    path('categories/', CategoryViewSet.as_view({'get': 'category_list'}), name='categories'),
    path('category/<int:pk>/', PostViewSet.as_view({'get': 'posts_list'}), name='posts'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'post_detail'}), name='post_detail'),
    path('sheikhs/', SheikhViewSet.as_view({'get': 'sheikh_list'}), name='sheikhs'),
    path('about/', AboutUsViewSet.as_view({'get': 'about_us'}), name='about_us'),
    path('verses/', VerseViewSet.as_view({'get': 'get_verses'}), name='verses'),
    path('sheikh/audio/<int:pk>/', SheikhViewSet.as_view({"get": 'sheikh_audio'}), name='sheikh_audio')
]
