from .models import Chapter, Verse, Category, Post, Sheikh, Audio, AboutUs
from rest_framework import serializers
from config import settings


class AudioSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['audio_translate'] = serializers.CharField(source=f'audio_translate_{language}')

    class Meta:
        model = Audio
        fields = ['id', 'sheikh', 'chapter', 'verse', 'audio', 'audio_translate']


class VerseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'description']


class ChapterListSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description']


class ChapterFullSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    verses = VerseSerializer(many=True, read_only=True, source='chapter_verse')

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'verses']


class VerseUzArabSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')

    audios = AudioSerializer(many=True, read_only=True, source='verse_audio')

    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'audios']


class VerseSearchSerializer(serializers.ModelSerializer):
    chapter_id = serializers.IntegerField(source='chapter.id', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)

    class Meta:
        model = Verse
        fields = ['id', 'number', 'chapter_id', 'chapter_name']


class ChapterUzArabSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    verses = VerseUzArabSerializer(many=True, read_only=True, source='chapter_verse')

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description', 'verses']


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
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
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'file', 'description', 'is_published', 'is_premium']


class SheikhSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = Sheikh
        fields = ['id', 'name']


class AboutUsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')

    class Meta:
        model = AboutUs
        fields = ['id', 'description']
