# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('websites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='domain',
            name='pagerank',
            field=models.FloatField(default=0),
        ),
    ]
