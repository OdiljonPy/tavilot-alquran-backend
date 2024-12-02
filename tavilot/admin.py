from django.contrib import admin
from .models import Chapter, Verse, Post, Category, AboutUs, Juz


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Verse)
class VerseAdmin(admin.ModelAdmin):
    list_display = ('id', 'chapter', 'text', 'text_arabic')
    list_display_links = ('id', 'chapter', 'text', 'text_arabic')
    search_fields = ('text', 'text_arabic')
    list_filter = ('chapter',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'file', 'is_published')
    list_display_links = ('id', 'category', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_published')



@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('description',)


@admin.register(Juz)
class JuzAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')
    list_display_links = ('id', 'number')
