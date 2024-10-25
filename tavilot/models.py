from django.db import models
from abstarct_model.base_model import BaseModel
from tinymce.models import HTMLField

class Chapter(BaseModel):
    name = models.CharField(max_length=150, verbose_name="название")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Глава'
        verbose_name_plural = 'Главы'
        ordering = ('-created_at',)

class Verse(BaseModel):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='глава')
    number = models.PositiveIntegerField(verbose_name="порядковый номер стиха")
    text = models.TextField(verbose_name="текст")
    text_arabic = models.TextField(verbose_name="текст на арабском языке")
    description = models.TextField(verbose_name="описание")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Стих'
        verbose_name_plural = 'Стихи'
        ordering = ('-created_at',)


class Sales(BaseModel):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

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
    app_updates = models.TextField(verbose_name="обновления приложений", blank=True, null=True)

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
    is_premium = models.BooleanField(default=False, verbose_name="это премиум")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)
