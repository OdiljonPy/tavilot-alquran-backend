from .models import Chapter, Verse, Category, Post, AboutUs, SubCategory, Juz
from rest_framework import serializers
from config import settings


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

    description = serializers.SerializerMethodField()

    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'description']

    def get_description(self, obj):
        return


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


class SubCategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = SubCategory
        fields = ['id', "category", 'name']


class CategorySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    subcategory = SubCategorySerializer(many=True, read_only=True, source='post_subcategory')

    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategory']


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
        fields = ['id', 'title', 'category', 'sub_category', 'file', 'description', 'is_published', 'is_premium',
                  'image']


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


class JuzSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')

    class Meta:
        model = Juz
        fields = ['id', 'number', 'title']


class VerseArabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'juz', 'chapter', 'number', 'text_arabic']


class ChapterArabSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

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
        fields = ['id', 'juz', 'name', 'description', 'number', 'verses']

    def get_verses(self, obj):
        juz = self.context.get('juz')
        if juz:
            verses = obj.chapter_verse.filter(juz=juz)
            return VerseArabSerializer(verses, many=True).data
        return []


class JuzArabSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')

    chapters = serializers.SerializerMethodField()

    class Meta:
        model = Juz
        fields = ['id', 'number', 'title', 'chapters']

    def get_chapters(self, obj):
        chapters = obj.juz_chapter.all()
        return ChapterArabSerializer(chapters, many=True, context={'juz': obj}).data


class VerseUzArabJuzSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')

    description = serializers.SerializerMethodField()

    class Meta:
        model = Verse
        fields = ['id', 'juz', 'chapter', 'number', 'text', 'text_arabic', 'description']

    def get_description(self, obj):
        return


class ChapterUzArabJuzSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

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
        fields = ['id', 'juz', 'name', 'description', 'number', 'verses']

    def get_verses(self, obj):
        juz = self.context.get('juz')
        if juz:
            verses = obj.chapter_verse.filter(juz=juz)
            return VerseUzArabJuzSerializer(verses, many=True).data
        return []


class JuzUzArabSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')

    class Meta:
        model = Juz
        fields = ['id', 'number', 'title', 'chapters']

    def get_chapters(self, obj):
        chapters = obj.juz_chapter.all()
        return ChapterUzArabJuzSerializer(chapters, many=True, context={'juz': obj}).data


class VerseFullJuzSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')
        print(f'description_{language}')

    class Meta:
        model = Verse
        fields = ['id', 'juz', 'chapter', 'number', 'text', 'text_arabic', 'description']


class ChapterFullJuzSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')
        self.fields['description'] = serializers.CharField(source=f'description_{language}')
        print(f'description_{language}')

    class Meta:
        model = Chapter
        fields = ['id', 'juz', 'name', 'description', 'number', 'verses']

    def get_verses(self, obj):
        juz = self.context.get('juz')
        if juz:
            verses = obj.chapter_verse.filter(juz=juz)
            return VerseFullJuzSerializer(verses, many=True).data
        return []


class JuzFullSerializer(serializers.ModelSerializer):
    chapters = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')

    class Meta:
        model = Juz
        fields = ['id', 'number', 'title', 'chapters']

    def get_chapters(self, obj):
        chapters = obj.juz_chapter.all()
        return ChapterFullJuzSerializer(chapters, many=True, context={'juz': obj}).data
