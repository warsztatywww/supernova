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
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> działający redis
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
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> działający redis
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Webpage',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
>>>>>>> działający redis
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
<<<<<<< HEAD
            field=models.ForeignKey(related_name='link_end', to='websites.Webpage'),
=======
            field=models.ForeignKey(to='websites.Webpage', related_name='link_end'),
>>>>>>> działający redis
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='link',
            name='start',
<<<<<<< HEAD
            field=models.ForeignKey(related_name='link_start', to='websites.Webpage'),
=======
            field=models.ForeignKey(to='websites.Webpage', related_name='link_start'),
>>>>>>> działający redis
            preserve_default=True,
        ),
    ]
