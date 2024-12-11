from django.core.validators import FileExtensionValidator
from django.db import models
from abstarct_model.base_model import BaseModel
from tinymce.models import HTMLField
from authentication.models import User
from django.core.exceptions import ValidationError

CHAPTER_TYPE_CHOICES = (
    (1, 'Makkiy'),
    (2, 'Madaniy')
)


class Juz(BaseModel):
    number = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=500)

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = 'Джуз'
        verbose_name_plural = 'Джузы'
        ordering = ['number']


class Chapter(BaseModel):
    juz = models.ManyToManyField(Juz, verbose_name='джуз', related_name='juz_chapter')
    name = models.CharField(max_length=150, verbose_name="название")
    name_arabic = models.CharField(max_length=150, verbose_name='название на арабском языке', blank=True, null=True)
    description = HTMLField(verbose_name="описание")
    verse_number = models.PositiveIntegerField(verbose_name='количество аятов', blank=True, null=True)
    number = models.PositiveIntegerField(unique=True)
    type_choice = models.IntegerField(choices=CHAPTER_TYPE_CHOICES, verbose_name='место ниспослания суры',
                                      blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сура'
        verbose_name_plural = 'Суры'
        ordering = ('number',)


class Verse(BaseModel):
    juz = models.ForeignKey(Juz, on_delete=models.CASCADE, verbose_name='джуз', related_name='juz_verse')
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='сура', related_name='chapter_verse')
    number = models.PositiveIntegerField(verbose_name="порядковый номер аят", db_index=True)
    text = models.TextField(verbose_name="аят", db_index=True)
    text_arabic = models.TextField(verbose_name="айат на арабском языке", db_index=True)
    description = HTMLField(verbose_name="описание аята")

    def __str__(self):
        return str(self.id)

    def clean(self):
        super().clean()
        if Verse.objects.select_related('chapter').filter(number=self.number,
                                                          chapter=self.chapter).exclude(id=self.id).exists():
            raise ValidationError("Аят с этой сурой и номером уже существует.")
        if not self.chapter.juz.filter(id=self.juz.id).exists():
            raise ValidationError("Джуз аята не соответствует джузу суры.")

    class Meta:
        verbose_name = 'Аят'
        verbose_name_plural = 'Аяты'
        ordering = ('number',)
        indexes = [
            models.Index(fields=['number'], name='number_index'),
            models.Index(fields=['text'], name='text_index'),
            models.Index(fields=['text_arabic'], name='text_arabic_index'),
        ]


class AboutUs(BaseModel):
    description = HTMLField(verbose_name='описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ('-created_at',)


class Moturudiy(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf',])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Мотуруди'
        verbose_name_plural = 'Мотуруди'
        ordering = ('-created_at',)


class Manuscript(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf',])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Рукопись и комментарии'
        verbose_name_plural = 'Рукописи и комментарии'
        ordering = ('-created_at',)



class Studies(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf',])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Исследовать'
        verbose_name_plural = 'Исследования'
        ordering = ('-created_at',)



class Resources(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf',])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Ресурс'
        verbose_name_plural = 'Ресурсы'
        ordering = ('-created_at',)


class Refusal(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf',])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Опровержение фанатизма'
        verbose_name_plural = 'Опровержение фанатизма'
        ordering = ('-created_at',)
