# Generated by Django 2.0.5 on 2018-06-03 04:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0024_extra_photo_valid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extra',
            name='photo_valid',
            field=models.NullBooleanField(verbose_name='校友卡证件照是否合格'),
        ),
    ]
