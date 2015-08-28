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
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='GitHubCache',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('github_path', models.CharField(max_length=255, unique=True)),
                ('fetched', models.DateTimeField(verbose_name='time fetched', default=django.utils.timezone.now)),
                ('json', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField()),
                ('homepage', models.URLField(max_length=255)),
                ('github_path', models.CharField(max_length=255, null=True, unique=True)),
                ('categories', models.ManyToManyField(to='search.Category')),
                ('github_data', models.ForeignKey(null=True, to='search.GitHubCache')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('homepage', models.URLField(max_length=255)),
                ('github_path', models.CharField(max_length=255, null=True, unique=True)),
                ('github_data', models.ForeignKey(null=True, to='search.GitHubCache')),
                ('organization', models.ForeignKey(null=True, to='search.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='search.Tag'),
        ),
    ]
