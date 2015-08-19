# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('cellID', models.AutoField(serialize=False, primary_key=True)),
                ('fileloc', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.SmallIntegerField()),
                ('controlCell', models.ForeignKey(related_name='control', to='cellcompdirector.Cell')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=300)),
                ('uname', models.CharField(max_length=100)),
                ('trustRating', models.DecimalField(max_digits=10, decimal_places=5)),
            ],
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(to='cellcompdirector.User'),
        ),
        migrations.AddField(
            model_name='rating',
            name='variableCell',
            field=models.ForeignKey(related_name='variable', to='cellcompdirector.Cell'),
        ),
    ]
