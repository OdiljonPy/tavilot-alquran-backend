# Generated by Django 5.1.2 on 2024-10-30 17:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavilot', '0004_rename_name_ru_category_name_kr_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aboutus',
            name='description_ar',
            field=models.TextField(null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='description_en',
            field=models.TextField(null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='description_kr',
            field=models.TextField(null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='description_tr',
            field=models.TextField(null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='aboutus',
            name='description_uz',
            field=models.TextField(null=True, verbose_name='описание'),
        ),
        migrations.AddField(
            model_name='sheikh',
            name='name_ar',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AddField(
            model_name='sheikh',
            name='name_en',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AddField(
            model_name='sheikh',
            name='name_kr',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AddField(
            model_name='sheikh',
            name='name_tr',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
        migrations.AddField(
            model_name='sheikh',
            name='name_uz',
            field=models.CharField(max_length=255, null=True, verbose_name='имя'),
        ),
    ]