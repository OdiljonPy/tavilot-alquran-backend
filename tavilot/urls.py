from django.urls import path
from .views import ChapterViewSet, AboutUsViewSet, VerseSearchViewSet, JuzViewSet, MoturudiyViewSet, ManuscriptViewSet, StudiesViewSet, ResourcesViewSet, RefusalViewSet

urlpatterns = [
    path('juz/', JuzViewSet.as_view({'get': 'get_juz'}), name='juz'),
    path('juz/<int:pk>/', JuzViewSet.as_view({'get': 'get_juz_detail'}), name='juz_detail'),
    path('chapters/', ChapterViewSet.as_view({'get': 'chapter_list'}), name='chapters'),
    path('chapter/<int:pk>/', ChapterViewSet.as_view({'get': 'chapter_detail'}),
         name='chapter_detail'),
    path('chapter/name/', ChapterViewSet.as_view({'post': 'chapter_bookmark'}), name='chapter_bookmark'),
    path('moturudiy/', MoturudiyViewSet.as_view({'get': 'moturudiy_posts_list'}), name='posts_about_moturudiy'),
    path('moturudiy/<int:pk>/', MoturudiyViewSet.as_view({'get': 'moturudiy_detail'}), name='moturudiy_detail'),
    path('manuscript/', ManuscriptViewSet.as_view({'get': 'manuscript_posts_list'}), name='posts_about_manuscript'),
    path('manuscript/<int:pk>/', ManuscriptViewSet.as_view({'get': 'manuscript_detail'}), name='manuscript_detail'),
    path('studies/', StudiesViewSet.as_view({'get': 'studies_posts_list'}), name='studies_posts_list'),
    path('studies/<int:pk>/', StudiesViewSet.as_view({'get': 'studies_detail'}), name='studies_detail'),
    path('resources/', ResourcesViewSet.as_view({'get': 'resources_posts_list'}), name='resources_posts_list'),
    path('resources/<int:pk>/', ResourcesViewSet.as_view({'get': 'resources_detail'}), name='resources_detail'),
    path('refusal/', RefusalViewSet.as_view({'get': 'refusal_posts_list'}), name='refusal_posts_list'),
    path('refusal/<int:pk>/', RefusalViewSet.as_view({'get': 'refusal_detail'}), name='refusal_detail'),
    path('about/', AboutUsViewSet.as_view({'get': 'about_us'}), name='about_us'),
    path('search/', VerseSearchViewSet.as_view({'get': 'search_verse'}), name='search_verse'),
]
