import os
import json

from django.core.management.base import BaseCommand, CommandError

from search import models
from . import _json_loader as json_loader

class Command(BaseCommand):
    help = 'Loads json data from specific locations into the database.'

    def handle(self, *args, **options):
        # load json into database, updating records where needed
        try:
            orgs_json = json.load(open(os.path.join(
                os.path.dirname(__file__),
                '../..',
                'frontend/organizations.json')
            ))
            projects_json = json.load(open(os.path.join(
                os.path.dirname(__file__),
                '../..',
                'frontend/projects.json')
            ))
            json_loader.fill_auxiliary(
                manager=models.Category,
                field='name',
                json=orgs_json,
                json_key='categories'
            )
            json_loader.fill_auxiliary(
                manager=models.Tag,
                field='name',
                json=projects_json,
                json_key='tags'
            )
            json_loader.fill_auxiliary(
                manager=models.License,
                field='name',
                json=projects_json,
                json_key='license'
            )
            json_loader.fill_models(
                manager=models.Organization,
                pk='id',
                json=orgs_json,
                attrs=(
                    'name',
                    'description',
                    {'name': 'homepage',   'default': ''},
                    {'name': 'categories', 'many_to_many': True, 'manager': models.Category, 'map_field': 'name'},
                    {'name': 'github_path', 'default': ''},
                ),
            )
            json_loader.fill_models(
                manager=models.Project,
                pk='id',
                json=projects_json,
                attrs=(
                    'name',
                    'description',
                    {'name': 'homepage',   'default': ''},
                    {'name': 'license', 'foreign_key_unique_name': True, 'manager': models.License, 'json_key': 'license'},
                    {'name': 'organization', 'foreign_key_id': True, 'manager': models.Organization, 'json_key': 'organizationId'},
                    {'name': 'tags', 'many_to_many': True, 'manager': models.Tag, 'map_field': 'name'},
                    {'name': 'github_path', 'default': ''},
                ),
            )
        except:
            raise CommandError('Bootstrapping from JSON failed. Not all data was loaded.')
