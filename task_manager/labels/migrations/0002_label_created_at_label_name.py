# Generated by Django 5.0.7 on 2024-08-20 14:25

import datetime
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='Date of creation'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='label',
            name='name',
            field=models.CharField(default=datetime.datetime(2024, 8, 20, 14, 25, 38, 884928, tzinfo=datetime.timezone.utc), max_length=150, unique=True, verbose_name='Name'),
            preserve_default=False,
        ),
    ]