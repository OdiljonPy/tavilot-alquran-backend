from django.contrib import admin
from .models import Chapter, Verse, AboutUs, Juz, Moturudiy, Manuscript, Studies, Resources, Refusal


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


@admin.register(Moturudiy)
class MoturudiyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'is_published')
    list_display_links = ('id', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)
    exclude = ('file_type',)


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'is_published')
    list_display_links = ('id', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)
    exclude = ('file_type',)


@admin.register(Studies)
class StudiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'is_published')
    list_display_links = ('id', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)
    exclude = ('file_type',)


@admin.register(Resources)
class ResourcesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'file', 'is_published')
    list_display_links = ('id', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)
    exclude = ('file_type',)


@admin.register(Refusal)
class RefusalAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'youtube_url', 'is_published')
    list_display_links = ('id', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('is_published',)


@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('description',)


@admin.register(Juz)
class JuzAdmin(admin.ModelAdmin):
    list_display = ('id', 'number')
    list_display_links = ('id', 'number')
