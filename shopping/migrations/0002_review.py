# Generated by Django 2.2.5 on 2019-11-08 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=1000)),
                ('rating', models.IntegerField(null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.Category')),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shopping.Product')),
            ],
        ),
    ]
