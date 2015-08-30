import os
import json

from django.core.management.base import BaseCommand, CommandError

from search.models import *
from . import _json_loader as json_loader

class Command(BaseCommand):
    help = 'Loads json data from specific locations into the database.'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        # load json into database, updating records where needed
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
            manager=Category,
            field='name',
            json=orgs_json,
            json_key='categories'
        )
        json_loader.fill_auxiliary(
            manager=Tag,
            field='name',
            json=projects_json,
            json_key='tags'
        )
        json_loader.fill_auxiliary(
            manager=License,
            field='name',
            json=projects_json,
            json_key='license'
        )
        json_loader.fill_models(
            manager=Organization,
            pk='id',
            json=orgs_json,
            attrs=(
                'name',
                'description',
                {'name': 'homepage',   'default': ''},
                {'name': 'categories', 'many_to_many': True, 'manager': Category, 'map_field': 'name'},
                {'name': 'github_path', 'default': ''},
            ),
        )
        json_loader.fill_models(
            manager=Project,
            pk='id',
            json=projects_json,
            attrs=(
                'name',
                'description',
                {'name': 'homepage',   'default': ''},
                {'name': 'license', 'foreign_key_unique_name': True, 'manager': License, 'json_key': 'license'},
                {'name': 'organization', 'foreign_key_id': True, 'manager': Organization, 'json_key': 'organizationId'},
                {'name': 'tags', 'many_to_many': True, 'manager': Tag, 'map_field': 'name'},
                {'name': 'github_path', 'default': ''},
            ),
        )
