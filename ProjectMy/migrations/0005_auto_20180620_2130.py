# Generated by Django 2.0.6 on 2018-06-20 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectMy', '0004_item_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='image',
        ),
        migrations.AddField(
            model_name='item',
            name='creation_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата создания'),
        ),
        migrations.AddField(
            model_name='item',
            name='is_sold',
            field=models.BooleanField(default=False, verbose_name='Продан'),
        ),
    ]
