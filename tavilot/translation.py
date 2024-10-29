from modeltranslation.translator import translator, TranslationOptions
from .models import Chapter, Verse, Category, Post, Sheikh, AboutUs, Audio


class ChapterTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class VerseTranslationOptions(TranslationOptions):
    fields = ('text', 'description')


class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

class SheikhTranslationOptions(TranslationOptions):
    fields = ('name',)

class AboutUsTranslationOptions(TranslationOptions):
    fields = ('description',)

class AudioTranslationOptions(TranslationOptions):
    fields = ('audio_translate',)


translator.register(Chapter, ChapterTranslationOptions)
translator.register(Verse, VerseTranslationOptions)
translator.register(Category, CategoryTranslationOptions)
translator.register(Post, PostTranslationOptions)
translator.register(Sheikh, SheikhTranslationOptions)
translator.register(AboutUs, AboutUsTranslationOptions)
