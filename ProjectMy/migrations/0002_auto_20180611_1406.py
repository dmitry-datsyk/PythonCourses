# Generated by Django 2.0.6 on 2018-06-11 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProjectMy', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='department',
            options={'verbose_name': 'Область', 'verbose_name_plural': 'Области'},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'verbose_name': 'Магазин', 'verbose_name_plural': 'Магазины'},
        ),
        migrations.AlterField(
            model_name='department',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='ProjectMy.Shop', verbose_name='ID магазина'),
        ),
        migrations.AlterField(
            model_name='department',
            name='sphere',
            field=models.CharField(max_length=100, verbose_name='Область'),
        ),
        migrations.AlterField(
            model_name='department',
            name='staff_amount',
            field=models.IntegerField(verbose_name='Количество сотрудников'),
        ),
        migrations.AlterField(
            model_name='item',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ProjectMy.Department', verbose_name='ID области'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.IntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='staff_amount',
            field=models.IntegerField(verbose_name='Количество сотрудников'),
        ),
    ]