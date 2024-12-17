from modeltranslation.translator import translator, TranslationOptions
from .models import Chapter, Verse, AboutUs, Juz, Moturudiy, Manuscript, Studies, Resources, Refusal


class ChapterTranslationOptions(TranslationOptions):
    fields = ('name', 'description')


class VerseTranslationOptions(TranslationOptions):
    fields = ('text', 'description')


class MoturudiyTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'file_name')


class ManuscriptTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'file_name')


class StudiesTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'file_name')


class ResourcesTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'file_name')


class RefusalTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


class AboutUsTranslationOptions(TranslationOptions):
    fields = ('description',)


class JuzTranslationOptions(TranslationOptions):
    fields = ('title',)


translator.register(Moturudiy, MoturudiyTranslationOptions)
translator.register(Chapter, ChapterTranslationOptions)
translator.register(Verse, VerseTranslationOptions)
translator.register(Manuscript, ManuscriptTranslationOptions)
translator.register(Studies, StudiesTranslationOptions)
translator.register(Resources, ResourcesTranslationOptions)
translator.register(Refusal, RefusalTranslationOptions)
translator.register(AboutUs, AboutUsTranslationOptions)
translator.register(Juz, JuzTranslationOptions)
