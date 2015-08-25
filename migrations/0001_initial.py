# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='GithubCache',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('github', models.CharField(unique=True, max_length=255)),
                ('fetched', models.DateTimeField(default=django.utils.timezone.now, verbose_name='time fetched')),
                ('json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
                ('description', models.TextField()),
                ('homepage', models.URLField(max_length=255)),
                ('github', models.CharField(null=True, unique=True, max_length=255)),
                ('categories', models.ManyToManyField(to='search.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('homepage', models.URLField(max_length=255)),
                ('github', models.CharField(null=True, unique=True, max_length=255)),
                ('github_data', models.ForeignKey(null=True, to='search.GithubCache')),
                ('organization', models.ForeignKey(null=True, to='search.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='search.Tag'),
        ),
    ]
