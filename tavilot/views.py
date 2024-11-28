from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import (Chapter, Category, Post, AboutUs, Verse, Juz)
from .serializers import (ChapterFullSerializer, PostSerializer,
                          ChapterListSerializer, CategorySerializer,
                          AboutUsSerializer, ChapterUzArabSerializer,
                          VerseSearchSerializer, ChapterIdNameSerializer,
                          JuzSerializer, ChapterIdSerializer,
                          JuzUzArabSerializer, JuzFullSerializer)


class JuzViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Juz',
        operation_description='List of Juz',
        responses={200: JuzSerializer(many=True)},
        tags=['Juz']
    )
    def get_juz(self, request):
        juz = Juz.objects.all()
        serializer = JuzSerializer(juz, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


    @swagger_auto_schema(
        operation_summary='Juz detail',
        operation_description='Juz detail with chapters and verses',
        responses={200: JuzUzArabSerializer()},
        tags=['Juz']
    )
    def get_juz_detail(self, request, pk):
        juz = Juz.objects.prefetch_related('juz_chapter', 'juz_verse').filter(id=pk).first()
        if juz is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        if request.user.rate and request.user.rate in [2]:
            serializer = JuzFullSerializer(juz, context={'request': request})
        else:
            serializer = JuzUzArabSerializer(juz, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ChapterViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of chapters',
        operation_description='List of chapters',
        responses={200: ChapterListSerializer(many=True)},
        tags=['Chapter'],
    )
    def chapter_list(self, request):
        chapter = Chapter.objects.all()
        serializer = ChapterListSerializer(chapter, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Chapter detail',
        operation_description='Chapter detail with verses',
        responses={200: ChapterFullSerializer()},
        tags=['Chapter'],
    )
    def chapter_detail(self, request, pk):
        chapter = Chapter.objects.prefetch_related('chapter_verse').filter(id=pk).first()
        if chapter is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        if request.user.rate and  request.user.rate in [2]:
            serializer = ChapterFullSerializer(chapter, context={'request': request})
        else:
            serializer = ChapterUzArabSerializer(chapter, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Chapter id list',
        operation_description='Chapter id list for bookmark',
        request_body=ChapterIdSerializer,
        responses={200: ChapterIdNameSerializer(many=True)},
        tags=['Chapter'],
    )
    def chapter_bookmark(self, request):
        ids = request.data.get('chapter_ids', [])
        chapter_objects = Chapter.objects.filter(id__in=ids)
        serializer = ChapterIdNameSerializer(chapter_objects, context={'request': request}, many=True)
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class VerseSearchViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING),
        ],
        operation_summary='Verse search',
        operation_description='Verse search with number, verse and verse arabic',
        responses={200: VerseSearchSerializer(many=True)},
        tags=['Search'],
    )
    def search_verse(self, request):
        filter_ = Q()
        q = request.query_params.get('q', None)
        if q:
            filter_ &= (Q(text__icontains=q) | Q(text_arabic__icontains=q) | Q(number__icontains=q))
        verses = Verse.objects.select_related('chapter').filter(filter_)
        serializer = VerseSearchSerializer(verses, many=True)
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class CategoryViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Category',
        operation_description='List of Category',
        responses={200: CategorySerializer(many=True)},
        tags=['Category'],
    )
    def category_list(self, request):
        category_list = Category.objects.all()
        serializer = CategorySerializer(category_list, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class PostViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts by category id',
        operation_description='List of posts by category id',
        responses={200: PostSerializer(many=True)},
        tags=['Post'],
    )
    def posts_list(self, request, pk):
        data = Post.objects.filter(category_id=pk, is_published=True)
        serializer = PostSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post',
        operation_description='Detail of post',
        responses={200: PostSerializer()},
        tags=['Post'],
    )
    def post_detail(self, request, pk):
        data = Post.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = PostSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class AboutUsViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='About Us',
        operation_description='About Us',
        responses={200: AboutUsSerializer()},
        tags=['AboutUs'],
    )
    def about_us(self, request):
        about_us = AboutUs.objects.order_by('-created_at').first()
        if about_us is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = AboutUsSerializer(about_us, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)
