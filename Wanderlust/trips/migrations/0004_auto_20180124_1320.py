# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 11:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_auto_20180124_1228'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='price',
        ),
        migrations.AddField(
            model_name='trip',
            name='adult_price',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trip',
            name='kid_price',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]