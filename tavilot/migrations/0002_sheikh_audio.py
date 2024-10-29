# Generated by Django 5.1.2 on 2024-10-29 16:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tavilot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sheikh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=255, verbose_name='имя')),
            ],
            options={
                'verbose_name': 'Шейх',
                'verbose_name_plural': 'Шейхи',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('audio', models.FileField(upload_to='audio/', verbose_name='голос')),
                ('audio_translate', models.FileField(upload_to='audio/', verbose_name='перевод голоса')),
                ('chapter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tavilot.chapter')),
                ('verse', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tavilot.verse')),
                ('sheikh', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tavilot.sheikh', verbose_name='')),
            ],
            options={
                'verbose_name': 'Голос',
                'verbose_name_plural': 'Голоса',
                'ordering': ('-created_at',),
            },
        ),
    ]