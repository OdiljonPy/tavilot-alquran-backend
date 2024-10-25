from .models import Chapter, Verse
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

class ParamValidateSerializer(serializers.Serializer):
    page = serializers.IntegerField(read_only=False, default=1)
    page_size = serializers.IntegerField(read_only=False, default=10)
    q = serializers.CharField(read_only=True)

    def validate(self, data):
        if data.get('page') and data.get('page') < 1 or data.get('page_size') and data.get('page_size') < 1:
            raise ValidationError('Page and page must be positive integers')
        return data

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description']

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'text', 'chapter', 'text_arabic', 'description']