from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import status
from drf_yasg import openapi
from .models import (Chapter, Category, Post, Sheikh, AboutUs, Verse, Audio)
from .serializers import (
    ChapterFullSerializer, PostSerializer, ChapterListSerializer,
    CategorySerializer, SheikhSerializer, AboutUsSerializer, ChapterUzArabSerializer, VerseSearchSerializer,
    AudioSerializer,
    VerseUzArabSerializer)
from drf_yasg.utils import swagger_auto_schema


class ChapterViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING),
        ],
        operation_summary='List of chapters',
        operation_description='List of chapters',
        responses={200: ChapterListSerializer(many=True)},
        tags=['Chapter'],
    )
    def chapter_list(self, request):
        chapter = Chapter.objects.all()
        return Response(
            data={'result': ChapterListSerializer(chapter, many=True, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Chapter detail with verses',
        operation_description='Chapter detail with verses',
        responses={200: ChapterFullSerializer()},
        tags=['Chapter'],
    )
    def chapter_detail(self, request, pk):
        chapter = Chapter.objects.prefetch_related('chapter_verse').filter(id=pk).first()
        if chapter is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response(data={'result': ChapterFullSerializer(chapter, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING),
        ],
        operation_summary='Chapter detail with arabic and translated verses',
        operation_description='Chapter detail with arabic and translated verses',
        responses={200: ChapterUzArabSerializer()},
        tags=['Chapter'],
    )
    def chapter_detail_translated_verses(self, request, pk):
        chapter = Chapter.objects.prefetch_related('chapter_verse').filter(id=pk).first()
        if chapter is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response(
            data={'result': ChapterUzArabSerializer(chapter, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)


class VerseFilterViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, description='Search query', type=openapi.TYPE_STRING),
        ],
        operation_summary='Searched verse with chapter id and name',
        operation_description='Searched verse with chapter id and name',
        responses={200: VerseSearchSerializer(many=True)},
        tags=['VerseSearch'],
    )
    def search_verse(self, request):
        filter_ = Q()
        q = request.query_params.get('q', None)
        if q:
            filter_ &= (Q(text__icontains=q) | Q(text_arabic__icontains=q) | Q(number__icontains=q))
        verses = Verse.objects.select_related('chapter').filter(filter_)
        return Response(data={'result': VerseSearchSerializer(verses, many=True).data, 'ok': True},
                        status=status.HTTP_200_OK)


class CategoryViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Category',
        operation_description='List of Category',
        responses={200: CategorySerializer(many=True)},
        tags=['Category'],
    )
    def category_list(self, request):
        category_list = Category.objects.all()
        return Response(data={'result': CategorySerializer(category_list, many=True, context={'request': request}).data,
                              'ok': True}, status=status.HTTP_200_OK)


class PostViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts by category id',
        operation_description='List of posts by category id',
        responses={200: PostSerializer(many=True)},
        tags=['Post'],
    )
    def posts_list(self, request, pk):
        data = Post.objects.filter(category_id=pk, is_published=True)
        return Response(data={'result': PostSerializer(data, many=True, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)

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
        return Response(data={'result': PostSerializer(data, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)


class SheikhViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of Sheikh',
        operation_description='List of Sheikh',
        responses={200: SheikhSerializer(many=True)},
        tags=['Sheikh'],
    )
    def sheikh_list(self, request):
        sheikh = Sheikh.objects.all()
        return Response(
            data={'result': SheikhSerializer(sheikh, many=True, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Sheikh's audios, pk receive Sheikh id",
        operation_description="Sheikh's audio, pk receive Sheikh id",
        responses={200: AudioSerializer(many=True)},
        tags=['Sheikh']
    )
    def sheikh_audio(self, request, pk):
        audio = Audio.objects.filter(sheikh_id=pk)
        serializer = AudioSerializer(audio, many=True, context={'request': request})
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
        return Response(data={'result': AboutUsSerializer(about_us, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)
