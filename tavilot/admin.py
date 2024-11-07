from django.contrib import admin
from .models import Chapter, Verse, Post, Category, AboutUs, SubCategory



class VerseTabularInline(admin.TabularInline):
    model = Verse
    extra = 1


class SubCategoryTabularInline(admin.TabularInline):
    model = SubCategory
    extra = 1


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    inlines = [VerseTabularInline]


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
    inlines = [SubCategoryTabularInline]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'file', 'is_premium', 'is_published')
    list_display_links = ('id', 'category', 'is_published')
    search_fields = ('title', 'description')
    list_filter = ('category', 'is_published', 'is_premium')



@admin.register(AboutUs)
class AboutUsAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('description',)
