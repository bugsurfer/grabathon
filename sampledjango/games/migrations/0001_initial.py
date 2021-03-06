# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-08 00:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Games',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=256)),
                ('min_players', models.IntegerField(default=0)),
                ('max_players', models.IntegerField(default=0)),
                ('pitch_amount', models.IntegerField(default=0)),
                ('start_time', models.DateTimeField()),
                ('duration', models.IntegerField(default=0)),
                ('user_type', models.CharField(max_length=256)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('user_ids', models.CharField(max_length=2056)),
                ('status', models.IntegerField(default=0)),
                ('pool_amount', models.IntegerField(default=0)),
                ('is_available', models.IntegerField(default=1)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Games')),
            ],
        ),
    ]
