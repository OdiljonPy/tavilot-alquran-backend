from django.core.paginator import Paginator
from django.db.models import Count
from tavilot.serializers import VerseUzArabSerializer, VerseArabSerializer

def get_verse_list(context: dict, page: int, page_size: int, version: int) -> dict:
    verses = context.get('verses')
    total_count = verses.aggregate(total_count=Count('id'))['total_count']
    pagination = Paginator(verses, page_size)
    page_obj = pagination.get_page(page)

    if version == 2:
        content = VerseUzArabSerializer(page_obj, many=True, context=context).data
    else:
        content = VerseArabSerializer(page_obj, many=True, context=context).data
    response = {
        'totalElements': total_count,
        'totalPages': pagination.num_pages,
        'size': page_size,
        'number': page,
        'numberOfElements': len(page_obj),
        'first': not page_obj.has_next(),
        'last': not page_obj.has_previous(),
        'empty': total_count == 0,
        'content': content
     }
    return response
