from django.db import models
from abstarct_model.base_model import BaseModel

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

