# Generated by Django 3.1.1 on 2021-03-24 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0011_remove_character_class_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='ladder',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]