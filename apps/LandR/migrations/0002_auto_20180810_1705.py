# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-08-10 21:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LandR', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=10),
        ),
    ]
