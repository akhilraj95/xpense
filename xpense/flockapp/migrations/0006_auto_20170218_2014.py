# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flockapp', '0005_auto_20170218_1959'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bills',
            name='image',
            field=models.ImageField(upload_to=b''),
        ),
    ]
