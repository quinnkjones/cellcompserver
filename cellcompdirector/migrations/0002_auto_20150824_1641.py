# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cellcompdirector', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rater',
            fields=[
                ('userId', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('trustRating', models.DecimalField(max_digits=10, decimal_places=5)),
            ],
        ),
        migrations.AlterField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(to='cellcompdirector.Rater'),
        ),
        migrations.DeleteModel(
            name='User',
        ),
        migrations.AddField(
            model_name='rater',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
