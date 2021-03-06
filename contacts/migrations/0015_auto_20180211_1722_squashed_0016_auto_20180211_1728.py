# Generated by Django 2.0.2 on 2018-02-11 09:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('contacts', '0015_auto_20180211_1722'), ('contacts', '0016_auto_20180211_1728')]

    dependencies = [
        ('contacts', '0014_auto_20180131_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clazz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
            ],
            options={
                'verbose_name': '班级',
                'verbose_name_plural': '班级',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=3, verbose_name='代码')),
                ('name', models.CharField(max_length=100, verbose_name='名称')),
            ],
            options={
                'verbose_name': '院系',
                'verbose_name_plural': '院系',
                'ordering': ['code'],
            },
        ),
        migrations.AddField(
            model_name='clazz',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contacts.Department', verbose_name='院系'),
        ),
    ]
