# Generated by Django 5.1.2 on 2024-10-18 00:22

import banjo.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tod',
            name='check_complete',
            field=banjo.models.BooleanField(default=False),
        ),
    ]
