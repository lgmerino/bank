# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-21 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankuser',
            name='iban',
            field=models.CharField(max_length=34, unique=True, verbose_name='IBAN'),
        ),
    ]
