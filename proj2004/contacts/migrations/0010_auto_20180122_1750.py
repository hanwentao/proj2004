# Generated by Django 2.0.1 on 2018-01-22 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0009_extra_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='industry',
            field=models.CharField(blank=True, max_length=100, verbose_name='所在行业'),
        ),
    ]