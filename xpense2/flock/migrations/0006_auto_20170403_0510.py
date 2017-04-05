# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 05:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flock', '0005_delete_groupmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='budget',
            field=models.IntegerField(blank=True, default=None),
        ),
        migrations.AddField(
            model_name='track',
            name='budget_currency',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flock.Currency'),
        ),
    ]