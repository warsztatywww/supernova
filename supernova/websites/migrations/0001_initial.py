# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('pagerank', models.FloatField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('path', models.CharField(max_length=4095)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=1023)),
                ('keywords', models.CharField(max_length=1023)),
                ('content', models.TextField()),
                ('domain', models.ForeignKey(to='websites.Domain')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='link',
            name='end',
            field=models.ForeignKey(related_name='link_end', to='websites.Webpage'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='start',
            field=models.ForeignKey(related_name='link_start', to='websites.Webpage'),
            preserve_default=True,
        ),
    ]
