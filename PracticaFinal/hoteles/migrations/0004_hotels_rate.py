# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-06-18 10:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoteles', '0003_configuration'),
    ]

    operations = [
        migrations.AddField(
            model_name='hotels',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
