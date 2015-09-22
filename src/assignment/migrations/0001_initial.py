# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import assignment.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_name', models.CharField(max_length=3)),
                ('rate', models.DecimalField(max_digits=8, decimal_places=2)),
            ],
            bases=(assignment.models.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
            ],
            bases=(assignment.models.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('amount', models.DecimalField(help_text='Default amount in USD', max_digits=8, decimal_places=2)),
                ('currency', models.ForeignKey(to='assignment.Currency')),
            ],
            options={
                'verbose_name': 'Service fee',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('fee', models.ForeignKey(to='assignment.Fee')),
            ],
            bases=(assignment.models.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('event', models.ForeignKey(related_name='products', to='assignment.Event')),
                ('product', models.ForeignKey(related_name='items', to='assignment.Product')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='fee',
            field=models.ForeignKey(to='assignment.Fee'),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
