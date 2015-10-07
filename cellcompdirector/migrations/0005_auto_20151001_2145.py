# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cellcompdirector', '0004_auto_20150922_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessioninfo',
            name='sessionRateAvg',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=5),
        ),
    ]
