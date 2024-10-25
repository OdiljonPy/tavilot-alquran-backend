from django.contrib import admin
from .models import Chapter, Verse

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']

@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ['id', 'chapter', 'text', 'text_arabic']
    list_display_links = ['id', 'chapter', 'text', 'text_arabic']
    search_fields = ['text', 'text_arabic']
