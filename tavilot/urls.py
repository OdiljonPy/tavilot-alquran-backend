from django.urls import path
from .views import ChapterViewSet, PostViewSet, CategoryViewSet, AboutUsViewSet, VerseSearchViewSet, JuzViewSet

urlpatterns = [
    path('juz/', JuzViewSet.as_view({'get': 'get_juz'}), name='juz'),
    path('juz/<int:pk>/', JuzViewSet.as_view({'get': 'get_juz_detail'}), name='juz_detail'),
    path('chapters/', ChapterViewSet.as_view({'get': 'chapter_list'}), name='chapters'),
    path('chapter/<int:pk>/', ChapterViewSet.as_view({'get': 'chapter_detail'}),
         name='chapter_detail'),
    path('chapter/name/', ChapterViewSet.as_view({'post': 'chapter_bookmark'}), name='chapter_bookmark'),
    path('categories/', CategoryViewSet.as_view({'get': 'category_list'}), name='categories'),
    path('category/<int:pk>/', PostViewSet.as_view({'get': 'posts_list'}), name='posts'),
    path('post/<int:pk>/', PostViewSet.as_view({'get': 'post_detail'}), name='post_detail'),
    path('about/', AboutUsViewSet.as_view({'get': 'about_us'}), name='about_us'),
    path('search/', VerseSearchViewSet.as_view({'get': 'search_verse'}), name='search_verse'),
]
