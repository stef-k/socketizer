# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-26 18:39
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainsite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Billing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchase_date', models.DateTimeField(auto_now_add=True)),
                ('domain_name', models.CharField(max_length=512, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('tax', models.DecimalField(decimal_places=2, max_digits=8)),
                ('days', models.IntegerField(default=0)),
                ('max_concurrent_users', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(default='', max_length=512)),
                ('api_key', models.CharField(default='', max_length=512)),
                ('free_key', models.BooleanField(default=False)),
                ('days_left', models.IntegerField(default=0)),
                ('max_concurrent_connections', models.IntegerField(default=0)),
                ('current_month_api_calls', models.IntegerField(default=0)),
                ('current_connections', models.IntegerField(default=0)),
                ('user_limits_last_update', models.DateTimeField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
