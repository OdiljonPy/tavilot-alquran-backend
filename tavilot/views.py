from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import status
from .models import (Chapter, Category, Post, Sheikh, AboutUs, Audio, Verse)
from .serializers import (
    ChapterFullSerializer, PostSerializer, ChapterListSerializer,
    CategorySerializer, SheikhSerializer, AboutUsSerializer, VerseUzArabSerializer, AudioSerializer)
from drf_yasg.utils import swagger_auto_schema


class ChapterViewSet(ViewSet):
    @swagger_auto_schema(
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
        chapter = Chapter.objects.prefetch_related('verse_set').filter(id=pk).first()
        if chapter is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response(data={'result': ChapterFullSerializer(chapter, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)


class VerseViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of verses',
        operation_description='List of verses',
        responses={200: VerseUzArabSerializer(many=True)},
        tags=['Verse'],
    )
    def get_verses(self, request, pk):
        verses = Verse.objects.filter(chapter_id=pk).order_by('number')
        return Response(
            data={'result': VerseUzArabSerializer(verses, many=True, context={'request': request}).data, 'ok': True},
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
