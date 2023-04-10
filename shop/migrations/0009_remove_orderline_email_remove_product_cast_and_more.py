# Generated by Django 4.1.6 on 2023-03-01 14:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_remove_orderline_name_orderline_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderline',
            name='email',
        ),
        migrations.RemoveField(
            model_name='product',
            name='cast',
        ),
        migrations.RemoveField(
            model_name='product',
            name='director',
        ),
        migrations.AddField(
            model_name='product',
            name='ves',
            field=models.IntegerField(blank=True, help_text='В шт.', null=True, verbose_name='Вес'),
        ),
        migrations.AlterField(
            model_name='product',
            name='play',
            field=models.IntegerField(blank=True, help_text='В шт.', null=True, verbose_name='Количество в упаковке'),
        ),
        migrations.AlterField(
            model_name='product',
            name='year',
            field=models.IntegerField(help_text='В днях', validators=[django.core.validators.MinValueValidator(30)], verbose_name='Срок годности'),
        ),
    ]
