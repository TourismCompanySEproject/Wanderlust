# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-24 12:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0005_auto_20180124_1409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='departing_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='returning_date',
            field=models.DateField(),
        ),
    ]
