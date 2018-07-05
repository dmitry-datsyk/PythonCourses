# Generated by Django 2.0.6 on 2018-06-07 19:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sphere', models.CharField(max_length=100)),
                ('staff_amount', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='ProjectMy.Department')),
            ],
        ),
        migrations.CreateModel(
            name='Shop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(max_length=300, null=True)),
                ('staff_amount', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='department',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departments', to='ProjectMy.Shop'),
        ),
    ]