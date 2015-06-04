# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dreams',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dream_subject', models.CharField(max_length=255, verbose_name=b'subject of dream')),
                ('dream_text', models.TextField(verbose_name=b'dream description')),
                ('dream_date', models.DateField(verbose_name=b'morning date')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('registration_date', models.DateTimeField(auto_now_add=True)),
                ('firstName', models.CharField(max_length=255)),
                ('lastName', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='dreams',
            name='user',
            field=models.ForeignKey(to='pools.User'),
        ),
    ]
