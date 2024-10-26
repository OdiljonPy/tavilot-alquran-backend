from .models import Chapter, Verse, Category, Post
from rest_framework import serializers
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes
from config import settings


class ParamValidateSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    q = serializers.CharField(required=False)
    type = serializers.IntegerField(required=True)

    def validate(self, data):
        if data.get('page') and data.get('page') < 1 or data.get('page_size') and data.get('page_size') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED,
                                     message='Page and page size should be a positive integer')
        if data.get('type') and data.get('type') not in [1, 2]:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Type should be 1 or 2')
        return data


class ChapterSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description']


class VerseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'description']

class VerseUzSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text']


class VerseArabicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text_arabic']


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = Category
        fields = ['id', 'name']


class PostSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'ru'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'file', 'description', 'is_published', 'is_premium']
