# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-21 12:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sgfood_app', '0004_restaurant_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
    ]