from .models import Chapter, Verse, AboutUs, Juz, Moturudiy, Manuscript, Studies, Resources, Refusal
from rest_framework import serializers
from config import settings
import html2text
from bs4 import BeautifulSoup


class ChapterListSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'number', 'name_arabic', 'verse_number', 'type_choice']


class VerseSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')

    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'description']


    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)
        if not description:
            description = ""

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data


class ChapterFullSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    verses = serializers.SerializerMethodField()
    def get_verses(self, obj):
        return VerseSerializer(obj.chapter_verse.all(), many=True, context=self.context).data

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'number', 'name_arabic', 'verse_number', 'type_choice', 'description', 'verses']

    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data


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


class ChapterUzArabSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    verses = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'name', 'number', 'name_arabic', 'verse_number', 'type_choice', 'description', 'verses']

    def get_verses(self, obj):
        return VerseUzArabSerializer(obj.chapter_verse.all(), many=True, context=self.context).data

    def get_description(self, obj):
        return


class VerseSearchSerializer(serializers.ModelSerializer):
    chapter_id = serializers.IntegerField(source='chapter.id', read_only=True)
    chapter_name = serializers.CharField(source='chapter.name', read_only=True)
    chapter_name_arabic = serializers.CharField(source='chapter.name_arabic', read_only=True)

    class Meta:
        model = Verse
        fields = ['id', 'number', 'chapter_id', 'chapter_name', 'chapter_name_arabic']


class MoturudiySerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['title'] = serializers.CharField(source=f'title_{language}')

    class Meta:
        model = Moturudiy
        fields = ['id', 'title', 'file','file_name', 'file_type', 'description', 'is_published']


    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data


class ManuscriptSerializer(MoturudiySerializer):
    class Meta:
        model = Manuscript
        fields = ['id', 'title', 'file', 'file_name','file_type', 'description', 'is_published']


class StudiesSerializer(MoturudiySerializer):
    class Meta:
        model = Studies
        fields = ['id', 'title', 'file', 'file_name', 'file_type', 'description', 'is_published']



class ResourcesSerializer(MoturudiySerializer):
    class Meta:
        model = Resources
        fields = ['id', 'title', 'file', 'file_name','file_type', 'description', 'is_published']



class RefusalSerializer(MoturudiySerializer):
    class Meta:
        model = Refusal
        fields = ['id', 'title', 'youtube_url', 'description', 'is_published']


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = ['id', 'description']


    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data


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

    description = serializers.SerializerMethodField()

    class Meta:
        model = Chapter
        fields = ['id', 'juz', 'name', 'name_arabic', 'verse_number', 'type_choice', 'description', 'number', 'verses']

    def get_description(self, obj):
        return

    def get_verses(self, obj):
        juz_id = self.context.get('juz_id')
        if juz_id:
            verses = obj.chapter_verse.filter(juz_id=juz_id)
            return VerseUzArabJuzSerializer(verses, many=True, context=self.context).data
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
        self.context['juz_id'] = obj.id
        return ChapterUzArabJuzSerializer(chapters, many=True, context=self.context).data


class VerseFullJuzSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['text'] = serializers.CharField(source=f'text_{language}')


    class Meta:
        model = Verse
        fields = ['id', 'juz', 'chapter', 'number', 'text', 'text_arabic', 'description']

    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)
        if not description:
            description = ""

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data



class ChapterFullJuzSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = Chapter
        fields = ['id', 'juz', 'name', 'name_arabic', 'verse_number', 'type_choice', 'description', 'number', 'verses']

    def get_verses(self, obj):
        juz_id = self.context.get('juz_id')
        if juz_id:
            verses = obj.chapter_verse.filter(juz_id=juz_id)
            return VerseFullJuzSerializer(verses, many=True, context=self.context).data
        return []

    def to_representation(self, instance):
        # Foydalanuvchi so'rovining til parametrini aniqlash
        request = self.context.get('request')
        language = 'uz'  # Standart til
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')

        # Dinamik tildagi `description` maydonini olish
        description_field = f'description_{language}'
        description = getattr(instance, description_field, instance.description)

        # Markdown formatiga aylantirish uchun HTMLni o'zgartirish
        soup = BeautifulSoup(description, "html.parser")

        # Rasmlar uchun Markdown formatini yaratish
        for img in soup.find_all("img"):
            base64_data = img.get("src")
            alt_text = img.get("alt", "image")  # Alt matn mavjud bo'lmasa "image"
            markdown_image = f"![{alt_text}]({base64_data})"
            img.replace_with(markdown_image)

        # HTMLdan Markdownga aylantirish
        markdown_converter = html2text.HTML2Text()
        markdown_converter.ignore_links = False
        markdown_description = markdown_converter.handle(str(soup))

        # Ma'lumotlarni qaytarish
        data = super().to_representation(instance)
        data['description'] = markdown_description
        return data


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
        self.context['juz_id'] = obj.id
        return ChapterFullJuzSerializer(chapters, many=True, context=self.context).data


class ChapterIdSerializer(serializers.Serializer):
    chapter_ids = serializers.ListField(child=serializers.IntegerField())


class ChapterIdNameSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        language = 'uz'
        if request and request.META.get('HTTP_ACCEPT_LANGUAGE') in settings.MODELTRANSLATION_LANGUAGES:
            language = request.META.get('HTTP_ACCEPT_LANGUAGE')
        self.fields['name'] = serializers.CharField(source=f'name_{language}')

    class Meta:
        model = Chapter
        fields = ('id', 'name')
