# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-09 09:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainsite', '0009_settings_max_connection'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='service_is_active',
            field=models.BooleanField(default=True, help_text='Enables - disables the websocket service'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='max_concurrent_connections',
            field=models.IntegerField(default=100, help_text='Domain limits'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='max_connection',
            field=models.IntegerField(default=5000, help_text='Server limits'),
        ),
        migrations.AlterField(
            model_name='settings',
            name='service_key',
            field=models.CharField(default='', help_text='A secret key to talk to websockets service', max_length=512),
        ),
    ]