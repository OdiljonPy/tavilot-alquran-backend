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


class Sales(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    item = models.CharField(max_length=150, verbose_name="элемент")
    price = models.FloatField(default=0, verbose_name="цена")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Продажa'
        verbose_name_plural = 'Продажи'
        ordering = ('-created_at',)


class AboutUs(BaseModel):
    description = HTMLField(verbose_name='описание')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ('-created_at',)


class Category(BaseModel):
    name = models.CharField(max_length=255, verbose_name='навзание')
    title = models.CharField(max_length=500, verbose_name='заголовок', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категория посты'
        ordering = ('-created_at',)


class SubCategory(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='post_subcategory',
                                 verbose_name="категория")
    name = models.CharField(max_length=255, verbose_name="название")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'
        ordering = ('-created_at',)


class Post(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, blank=True, null=True,
                                     verbose_name="подкатегория")
    title = models.CharField(max_length=300, verbose_name="заголовок")
    image = models.ImageField(upload_to='post/', verbose_name='изображение')
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'zip'])])
    file_type = models.CharField(max_length=10, blank=True, null=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")
    is_premium = models.BooleanField(default=False, verbose_name="премиум")

    def clean(self):
        super().clean()
        self.file_type = str(self.file.name).split('.')[-1]
        self.save()


    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)
