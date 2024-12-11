from django.db.models import Q

from rest_framework import status
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .models import (Chapter, AboutUs, Verse, Juz, Moturudiy,
                     Manuscript, Studies, Resources, Refusal)

from .serializers import (ChapterFullSerializer, MoturudiySerializer,
                          ManuscriptSerializer, StudiesSerializer,
                          ResourcesSerializer, RefusalSerializer,
                          ChapterListSerializer,
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
        user = request.user
        if juz is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        if getattr(user, 'rate', None) and user.rate in [2]:
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
        user = request.user
        if chapter is None:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        if getattr(user, 'rate', None) and  user.rate in [2]:
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


class MoturudiyViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts about Moturudiy',
        operation_description='List of posts about Moturudiy',
        responses={200: MoturudiySerializer(many=True)},
        tags=['Moturudiy'],
    )
    def moturudiy_posts_list(self, request):
        data = Moturudiy.objects.filter(is_published=True)
        serializer = MoturudiySerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post about Moturudiy',
        operation_description='Detail of post about Moturudiy',
        responses={200: MoturudiySerializer()},
        tags=['Moturudiy'],
    )
    def moturudiy_detail(self, request, pk):
        data = Moturudiy.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = MoturudiySerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ManuscriptViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts about Manuscript',
        operation_description='List of posts about Manuscript',
        responses={200: ManuscriptSerializer(many=True)},
        tags=['Manuscript'],
    )
    def manuscript_posts_list(self, request):
        data = Manuscript.objects.filter(is_published=True)
        serializer = ManuscriptSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post about Manuscript',
        operation_description='Detail of post about Manuscript',
        responses={200: ManuscriptSerializer()},
        tags=['Manuscript'],
    )
    def manuscript_detail(self, request, pk):
        data = Manuscript.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ManuscriptSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class StudiesViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts about Studies',
        operation_description='List of posts about Studies',
        responses={200: StudiesSerializer(many=True)},
        tags=['Studies'],
    )
    def studies_posts_list(self, request):
        data = Studies.objects.filter(is_published=True)
        serializer = StudiesSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post about Studies',
        operation_description='Detail of post about Studies',
        responses={200: StudiesSerializer()},
        tags=['Studies'],
    )
    def studies_detail(self, request, pk):
        data = Studies.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = StudiesSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class ResourcesViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts about Resources',
        operation_description='List of posts about Resources',
        responses={200: ResourcesSerializer(many=True)},
        tags=['Resources'],
    )
    def resources_posts_list(self, request):
        data = Resources.objects.filter(is_published=True)
        serializer = ResourcesSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post about Resources',
        operation_description='Detail of post about Resources',
        responses={200: ResourcesSerializer()},
        tags=['Resources'],
    )
    def resources_detail(self, request, pk):
        data = Resources.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = ResourcesSerializer(data, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)


class RefusalViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary='List of posts about Refusal',
        operation_description='List of posts about Refusal',
        responses={200: RefusalSerializer(many=True)},
        tags=['Refusal'],
    )
    def refusal_posts_list(self, request):
        data = Refusal.objects.filter(is_published=True)
        serializer = RefusalSerializer(data, many=True, context={'request': request})
        return Response(data={'result': serializer.data, 'ok': True}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary='Detail of post about Refusal',
        operation_description='Detail of post about Refusal',
        responses={200: RefusalSerializer()},
        tags=['Refusal'],
    )
    def refusal_detail(self, request, pk):
        data = Refusal.objects.filter(id=pk, is_published=True).first()
        if not data:
            raise CustomApiException(ErrorCodes.NOT_FOUND)
        serializer = RefusalSerializer(data, context={'request': request})
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
