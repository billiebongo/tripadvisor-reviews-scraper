# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-21 11:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sgfood_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurant',
            name='url',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='rest_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='review',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='sgfood_app.Restaurant'),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_body',
            field=models.CharField(max_length=500),
        ),
    ]
