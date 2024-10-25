from .models import Chapter, Verse
from rest_framework import serializers
from exception.exceptions import CustomApiException
from exception.error_message import ErrorCodes

class ParamValidateSerializer(serializers.Serializer):
    page = serializers.IntegerField(required=False, default=1)
    page_size = serializers.IntegerField(required=False, default=10)
    q = serializers.CharField(required=False)

    def validate(self, data):
        if data.get('page') and data.get('page') < 1 or data.get('page_size') and data.get('page_size') < 1:
            raise CustomApiException(ErrorCodes.VALIDATION_FAILED, message='Page and page size should be a positive integer')
        return data

class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'name', 'description']

class VerseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verse
        fields = ['id', 'chapter', 'number', 'text', 'text_arabic', 'description']