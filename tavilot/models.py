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
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name='')

    text = models.TextField(verbose_name="")
    text_arabic = models.TextField(verbose_name="")
    description = models.TextField(verbose_name="")

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)


class Sales(BaseModel):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)

    item = models.CharField(max_length=150, verbose_name="")
    price = models.FloatField(default=0)

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)

class AboutUs(BaseModel):
    description = models.TextField(verbose_name="")
    app_updates = models.TextField(verbose_name="", blank=True, null=True)

    def __str__(self):
        return str(self.id) or ''

    class Meta:
        verbose_name = ''
        verbose_name_plural = ''
        ordering = ('-created_at',)

