# Generated by Django 3.1.1 on 2021-03-27 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0015_auto_20210327_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='amulet',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='anni',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='armor',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='belt',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='boots',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='charms',
            field=models.CharField(blank=True, default=None, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='gloves',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='helmet',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='left_ring',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='main_hand',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='off_hand',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='right_ring',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='switch_main_hand',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='switch_off_hand',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='equipment',
            name='torch',
            field=models.CharField(blank=True, default=None, max_length=10, null=True),
        ),
    ]