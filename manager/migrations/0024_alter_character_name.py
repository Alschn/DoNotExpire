# Generated by Django 4.1.1 on 2022-10-03 11:05

import django.core.validators
from django.db import migrations, models
import manager.validators


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0023_alter_character_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z\\_]{2,15}$', "Character's name should consist of letters only and up to one underscore. It should be between 2 and 15 characters. "), manager.validators.underscore_validator]),
        ),
    ]
