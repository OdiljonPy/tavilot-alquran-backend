from django.contrib import admin
from .models import Chapter, Verse, Post, Category


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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    search_fields = ['name']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'file', 'is_premium', 'is_published']
    list_display_links = ['id', 'category', 'is_published']
