# Generated by Django 2.2.5 on 2019-11-10 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sports', '0014_auto_20191109_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='sport_info',
            name='objective',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='sport_info',
            name='scoring',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='sport_info',
            name='rules',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]
