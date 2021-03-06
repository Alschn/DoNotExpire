# Generated by Django 3.1.1 on 2021-05-01 19:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0016_auto_20210327_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='name',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z\\.\\-\\_]{2,15}', 'Account name should consist of alphanumerics and ".", "-", "_" signs')]),
        ),
        migrations.AlterField(
            model_name='character',
            name='name',
            field=models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[a-zA-Z]{2,15}$', 'Character name should consist of letters only.')]),
        ),
    ]
