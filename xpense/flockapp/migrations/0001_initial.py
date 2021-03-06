# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 09:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='user', max_length=30)),
                ('chatId', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ChatExpense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0.0)),
                ('purpose', models.CharField(default='Unspecified', max_length=100)),
                ('equallyshared', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Chattrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('user', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.Chat')),
            ],
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('abbr', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('amount', models.FloatField(default=0.0)),
                ('purpose', models.CharField(default='Unspecified', max_length=100)),
                ('equallyshared', models.BooleanField(default=False)),
                ('currency', models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.Currency')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='user', max_length=30)),
                ('userId', models.CharField(max_length=100)),
                ('token', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='track',
            name='user',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.User'),
        ),
        migrations.AddField(
            model_name='expense',
            name='paidby',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.User'),
        ),
        migrations.AddField(
            model_name='expense',
            name='track',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.Track'),
        ),
        migrations.AddField(
            model_name='chatexpense',
            name='currency',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.Currency'),
        ),
        migrations.AddField(
            model_name='chatexpense',
            name='paidby',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.User'),
        ),
        migrations.AddField(
            model_name='chatexpense',
            name='track',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='flockapp.Chattrack'),
        ),
    ]
