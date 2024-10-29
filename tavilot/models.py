from django.db import models
from abstarct_model.base_model import BaseModel
from tinymce.models import HTMLField
from authentication.models import User

class Chapter(BaseModel):
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Сура'
        verbose_name_plural = 'Суры'
        ordering = ('-created_at',)

class Verse(BaseModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='сура')
    number = models.PositiveIntegerField(verbose_name="порядковый номер айат")
    text = models.TextField(verbose_name="айат")
    text_arabic = models.TextField(verbose_name="айат на арабском языке")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Айат'
        verbose_name_plural = 'Айаты'
        ordering = ('-created_at',)


class Sales(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    item = models.CharField(max_length=150, verbose_name="элемент")
    price = models.FloatField(default=0, verbose_name="цена")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Продажa'
        verbose_name_plural = 'Продажи'
        ordering = ('-created_at',)

class AboutUs(BaseModel):
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'О нас'
        verbose_name_plural = 'О нас'
        ordering = ('-created_at',)


class Category(BaseModel):
    name = models.CharField(max_length=500, verbose_name='навзание')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория поста'
        verbose_name_plural = 'Категория посты'
        ordering = ('-created_at',)


class Post(BaseModel):
    title = models.CharField(max_length=300, verbose_name="заголовок")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="категория")
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True)
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")
    is_premium = models.BooleanField(default=False, verbose_name="премиум")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)


class Sheikh(BaseModel):
    name = models.CharField(max_length=255, verbose_name="имя")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Шейх'
        verbose_name_plural = 'Шейхи'
        ordering = ('-created_at',)

class Audio(BaseModel):
    sheikh = models.ForeignKey(Sheikh, on_delete=models.CASCADE, verbose_name='')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, blank=True, null=True)
    verse = models.ForeignKey(Verse, on_delete=models.SET_NULL, blank=True, null=True)

    audio = models.FileField(upload_to="audio/", verbose_name='голос')
    audio_translate = models.FileField(upload_to='audio/', verbose_name='перевод голоса')

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Голос'
        verbose_name_plural = 'Голоса'
        ordering = ('-created_at',)
