# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cellcompdirector', '0002_auto_20150824_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='SessionInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sessionRateAvg', models.DecimalField(default=0.0, max_digits=5, decimal_places=5)),
                ('sessionCount', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='rater',
            name='ratingCount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rater',
            name='ratingRateAvg',
            field=models.DecimalField(default=0.0, max_digits=5, decimal_places=5),
        ),
        migrations.AlterField(
            model_name='rater',
            name='trustRating',
            field=models.DecimalField(default=0.0, max_digits=10, decimal_places=5),
        ),
        migrations.AddField(
            model_name='sessioninfo',
            name='user',
            field=models.ForeignKey(related_name='sessions', to='cellcompdirector.Rater'),
        ),
    ]
