from django.db.models import Q
from .repository.get_filtered_verses import get_verse_list
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .models import Chapter, Verse
from .serializers import ChapterSerializer, ParamValidateSerializer

class ChapterViewSet(ViewSet):
    def chapter_list(self, request):
        chapter = Chapter.objects.all()
        return Response(data={'result': ChapterSerializer(chapter, many=True, context={'request': request}).data, 'ok': True}, status=status.HTTP_200_OK)

    # def chapter_detail(self, request, pk):
    #     chapter = Chapter.objects.filter(pk=pk).first()
    #     if not chapter:
    #         raise ValidationError('No chapter exists')
    #     return Response(data={'result': ChapterSerializer(chapter, context={'request': request}).data, 'ok': True}, status=status.HTTP_200_OK)


class VerseViewSet(ViewSet):
    def verse_list(self, request, pk):
        params = request.query_params
        serializer = ParamValidateSerializer(data=params, context={'request': request})
        if not serializer.is_valid():
            raise ValidationError(serializer.errors)
        q = serializer.validated_data.get('q', '')
        filter_ = Q()
        if q:
            filter_ &= (Q(text__icontains=q) | Q(text_arabic__icontains=q | Q(number__icontains=q)))
        verses = Verse.objects.filter(chapter_id=pk).filter(filter_)
        response = get_verse_list(context={'request': request, 'verses': verses}, page=serializer.data.get('page', 1),
                                 page_size=serializer.data.get('page_size', 10))
        return Response(data={'result': response, 'ok': True}, status=status.HTTP_200_OK)

    # def verse_detail(self, request, pk):
    #     verse = Verse.objects.filter(id=pk).filter()
    #     if not verse:
    #         raise ValidationError('No verse exists')
    #     return Response(data={'result': VerseSerializer(verse, context={'request': request}).data, 'ok': True}, status=status.HTTP_200_OK)
