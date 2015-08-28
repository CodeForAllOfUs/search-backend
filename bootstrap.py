import os
import json

from . import json_loader
from .models import *

# load json into database, updating records where needed
orgs_json = json.load(open(os.path.join(
    os.path.dirname(__file__),
    'frontend/organizations.json')
))
projects_json = json.load(open(os.path.join(
    os.path.dirname(__file__),
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
json_loader.fill_models(
    manager=Organization,
    pk='id',
    json=orgs_json,
    attrs=(
        'name',
        'description',
        {'name': 'homepage',   'default': ''},
        {'name': 'github_path', 'default': ''},
        {'name': 'categories', 'many_to_many': True, 'manager': Category, 'map_field': 'name'}
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
        {'name': 'github_path', 'default': ''},
        {'name': 'tags', 'many_to_many': True, 'manager': Tag, 'map_field': 'name'},
        {'name': 'organization', 'foreign_key': True, 'manager': Organization, 'json_key': 'organizationId'}
    ),
)
