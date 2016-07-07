# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-03 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0006_remove_domain_current_connections'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='domain',
            name='free_key',
        ),
        migrations.AlterField(
            model_name='domain',
            name='domain',
            field=models.CharField(default='', max_length=512, unique=True),
        ),
    ]
