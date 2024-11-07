from modeltranslation.translator import translator, TranslationOptions
from .models import Chapter, Verse, Category, Post, AboutUs


class ChapterTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class VerseTranslationOptions(TranslationOptions):
    fields = ('text', 'description')


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class AboutUsTranslationOptions(TranslationOptions):
    fields = ('description',)


translator.register(Chapter, ChapterTranslationOptions)
translator.register(Verse, VerseTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(AboutUs, AboutUsTranslationOptions)
