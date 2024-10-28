from django.db.models import Q
from .repository.get_filtered_verses import get_verse_list
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import status
from .models import (Chapter, Verse,
                     Category, Post)
from .serializers import (
    ChapterSerializer, ParamValidateSerializer,
    VerseSerializer, PostSerializer,
    CategorySerializer)
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ChapterViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of chapters',
        operation_description='List of chapters',
        responses={200: ChapterSerializer(many=True)},
        tags=['Chapter'],
    )
    def chapter_list(self, request):
        chapter = Chapter.objects.all()
        return Response(
            data={'result': ChapterSerializer(chapter, many=True, context={'request': request}).data, 'ok': True},
            status=status.HTTP_200_OK)


class VerseViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                              description='Page size'),
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search query')
        ],
        operation_summary='List of verses by chapter id',
        operation_description='List of verses by chapter id',
        responses={200: VerseSerializer(many=True)},
        tags=['Verse'],
    )
    def verse_list(self, request, pk):
        params = request.query_params
        serializer = ParamValidateSerializer(data=params, context={'request': request})
        if not serializer.is_valid():
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, serializer.errors)
        q = serializer.validated_data.get('q', '')
        filter_ = Q()
        if q:
            filter_ &= (Q(text__icontains=q) | Q(text_arabic__icontains=q) | Q(number__icontains=q))
        verses = Verse.objects.filter(filter_, chapter_id=pk)
        response = get_verse_list(context={'request': request, 'verses': verses},
                                  page=serializer.validated_data.get('page', 1),
                                  page_size=serializer.validated_data.get('page_size', 10))
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Verse detail',
        operation_description='Verse detail for premium user',
        responses={200: VerseSerializer()},
        tags=['Verse'],
    )
    def verse_detail(self, request, pk):
        verse = Verse.objects.filter(id=pk).first()
        if not verse:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response(data={'result': VerseSerializer(verse, context={'request': request}).data, 'ok': True},
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
        responses={200: ChapterSerializer()},
        tags=['Post'],
    )
    def post_detail(self, request, pk):
        data = Post.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        return Response(data={'result': PostSerializer(data, context={'request': request}).data, 'ok': True},
                        status=status.HTTP_200_OK)
