# Generated by Django 2.2.5 on 2019-09-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('winning_criteria', models.TextField(max_length=1000, null=True)),
                ('rules', models.TextField(max_length=1000, null=True)),
                ('objective', models.TextField(max_length=1000, null=True)),
            ],
        ),
    ]
