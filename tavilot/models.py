from django.core.validators import FileExtensionValidator
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
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='сура', related_name='chapter_verse')
    number = models.PositiveIntegerField(verbose_name="порядковый номер аят", db_index=True)
    text = models.TextField(verbose_name="аят", db_index=True)
    text_arabic = models.TextField(verbose_name="айат на арабском языке", db_index=True)
    description = models.TextField(verbose_name="описание аята")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Аят'
        verbose_name_plural = 'Аяты'
        ordering = ('-created_at',)
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
    image = models.ImageField(upload_to='post/', verbose_name='изображение')
    file = models.FileField(upload_to='to_students/', verbose_name="файл", null=True, blank=True,
                            validators=[FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'zip'])])
    description = HTMLField(verbose_name='описание')
    is_published = models.BooleanField(default=False, verbose_name="опубликовано")
    is_premium = models.BooleanField(default=False, verbose_name="премиум")

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('-created_at',)
