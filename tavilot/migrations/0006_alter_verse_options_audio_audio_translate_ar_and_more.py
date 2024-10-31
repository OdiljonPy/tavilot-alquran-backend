# Generated by Django 5.1.2 on 2024-10-31 04:56

import django.core.validators
import django.db.models.deletion
import tinymce.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavilot', '0005_aboutus_description_ar_aboutus_description_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='verse',
            options={'ordering': ('-created_at',), 'verbose_name': 'Аят', 'verbose_name_plural': 'Аяты'},
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_translate_ar',
            field=models.FileField(null=True, upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_translate_en',
            field=models.FileField(null=True, upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_translate_kr',
            field=models.FileField(null=True, upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_translate_tr',
            field=models.FileField(null=True, upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AddField(
            model_name='audio',
            name='audio_translate_uz',
            field=models.FileField(null=True, upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description',
            field=tinymce.models.HTMLField(verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description_ar',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description_en',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description_kr',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description_tr',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='aboutus',
            name='description_uz',
            field=tinymce.models.HTMLField(null=True, verbose_name='описание'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='audio',
            field=models.FileField(upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='голос'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='audio_translate',
            field=models.FileField(upload_to='audio/', validators=[django.core.validators.FileExtensionValidator(['mp3', 'wav', 'flac', 'ogg', 'm4a'])], verbose_name='перевод голоса'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tavilot.chapter', verbose_name='сура'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='sheikh',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tavilot.sheikh', verbose_name='шейх'),
        ),
        migrations.AlterField(
            model_name='audio',
            name='verse',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='verse_audio', to='tavilot.verse', verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='post',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='to_students/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'])], verbose_name='файл'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='chapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapter_verse', to='tavilot.chapter', verbose_name='сура'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description',
            field=models.TextField(verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description_ar',
            field=models.TextField(null=True, verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description_en',
            field=models.TextField(null=True, verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description_kr',
            field=models.TextField(null=True, verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description_tr',
            field=models.TextField(null=True, verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='description_uz',
            field=models.TextField(null=True, verbose_name='описание аята'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='number',
            field=models.PositiveIntegerField(verbose_name='порядковый номер аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text',
            field=models.TextField(verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text_ar',
            field=models.TextField(null=True, verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text_en',
            field=models.TextField(null=True, verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text_kr',
            field=models.TextField(null=True, verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text_tr',
            field=models.TextField(null=True, verbose_name='аят'),
        ),
        migrations.AlterField(
            model_name='verse',
            name='text_uz',
            field=models.TextField(null=True, verbose_name='аят'),
        ),
    ]