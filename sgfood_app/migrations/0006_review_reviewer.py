# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-27 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgfood_app', '0005_auto_20180321_1237'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='reviewer',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
