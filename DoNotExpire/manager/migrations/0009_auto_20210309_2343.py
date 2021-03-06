# Generated by Django 3.1.1 on 2021-03-09 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0008_auto_20210309_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='expansion',
            field=models.BooleanField(blank=True, default=True, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='hardcore',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='character',
            name='last_visited',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
