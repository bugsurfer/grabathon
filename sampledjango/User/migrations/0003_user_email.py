# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2019-12-07 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0002_userbalance'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.CharField(default='', max_length=256),
        ),
    ]
