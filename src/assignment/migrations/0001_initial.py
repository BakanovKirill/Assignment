# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import assignment.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=3)),
                ('rate', models.DecimalField(max_digits=6, decimal_places=4)),
            ],
            options={
                'verbose_name_plural': 'Currencies',
            },
            bases=(assignment.models.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('total', models.DecimalField(null=True, max_digits=10, decimal_places=2, blank=True)),
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
                ('fee', models.ForeignKey(blank=True, to='assignment.Fee', null=True)),
            ],
            bases=(assignment.models.UnicodeNameMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ProductItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('event', models.ForeignKey(related_name='product_items', to='assignment.Event')),
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
            name='products',
            field=models.ManyToManyField(to='assignment.Product', through='assignment.ProductItem'),
        ),
    ]
