# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cellcompdirector', '0003_auto_20150922_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rater',
            name='ratingRateAvg',
            field=models.DecimalField(default=0.0, max_digits=11, decimal_places=5),
        ),
    ]
