# Generated by Django 4.1.6 on 2023-03-12 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0020_rename_otziv_review_rev'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]
