# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='githubcache',
            name='github_url',
            field=models.URLField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='github_url',
            field=models.URLField(unique=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='organization',
            name='homepage',
            field=models.URLField(max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='github_url',
            field=models.URLField(unique=True, null=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='project',
            name='homepage',
            field=models.URLField(max_length=255),
        ),
    ]
