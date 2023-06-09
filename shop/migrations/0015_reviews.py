# Generated by Django 4.1.6 on 2023-03-08 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_delete_blogcomment_delete_blogpost'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name='Имя')),
                ('surname', models.CharField(max_length=70, null=True, verbose_name='Фамилия')),
                ('email', models.EmailField(max_length=254)),
                ('review', models.TextField(blank=True, verbose_name='Отзыв покупателя')),
            ],
        ),
    ]
