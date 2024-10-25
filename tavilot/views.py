from django.db.models import Q
from .repository.get_filtered_verses import get_verse_list
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from rest_framework import status
from .models import Chapter, Verse
from .serializers import ChapterSerializer, ParamValidateSerializer, VerseSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class ChapterViewSet(ViewSet):
    @swagger_auto_schema(
        operation_summary = 'List of chapters',
        operation_description = 'List of chapters',
        responses={200: ChapterSerializer(many=True)},
        tags=['Chapter'],
    )
    def chapter_list(self, request):
        chapter = Chapter.objects.all()
        return Response(data={'result': ChapterSerializer(chapter, many=True, context={'request': request}).data, 'ok': True}, status=status.HTTP_200_OK)


class VerseViewSet(ViewSet):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(name='page', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page number'),
            openapi.Parameter(name='page_size', in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER, description='Page size'),
            openapi.Parameter(name='q', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Search query'),
        ],
        operation_summary = 'List of verses by chapter id',
        operation_description = 'List of verses by chapter id',
        responses = {200: VerseSerializer(many=True)},
        tags = ['Verse'],
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
        response = get_verse_list(context={'request': request, 'verses': verses}, page=serializer.data.get('page', 1),
                                 page_size=serializer.data.get('page_size', 10))
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    # def verse_detail(self, request, pk):
    #     verse = Verse.objects.filter(id=pk).filter()
    #     if not verse:
    #         raise CustomApiException(ErrorCodes.NOT_FOUND)
    #     return Response(data={'result': VerseSerializer(verse, context={'request': request}).data, 'ok': True}, status=status.HTTP_200_OK)
