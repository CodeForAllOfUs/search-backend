import os
import json

from .models import *

# see if you can make this module run *after* the server is started, with some kinda django hook
# then query the GitHub API as much as you can for the *most stale* data
# (sort data by most stale first and iterate until you run out of rate limit)
# take a second in between requests to not flood GitHub's servers

organizations = json.load(open(os.path.join(os.path.dirname(__file__), 'frontend/organizations.json')))
projects = json.load(open(os.path.join(os.path.dirname(__file__), 'frontend/projects.json')))

saved_categories = {cat.name: cat for cat in Category.objects.all()}
saved_tags = {tag.name: tag for tag in Tag.objects.all()}

def fill_auxiliary(Manager, saved, data, key):
    """
    gather all categories/tags, then fill the database with any new ones
    """
    unsaved = set()

    for d in data:
        unsaved.update(d[key])

    unsaved = unsaved - set(saved.keys())

    for name in unsaved:
        saved[name] = Manager.objects.create(name=name)

def fill_organizations():
    """
    create all groups with the appropriate categories
    """
    for o in organizations:
        try:
            org = Organization.objects.get(pk=o['id'])
        except:
            org = Organization()

        # update properties
        org.name = o['name']
        org.description = o['description']
        org.homepage    = o.get('homepage', '')
        org.github_url  = o.get('github_url', '')

        # save org before we start modifying its ManyToManyField
        # ref: https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/
        org.save()
        org.categories.add(*(saved_categories[cat] for cat in o['categories']))

def fill_projects():
    """
    create all projects with the appropriate tags
    """
    for p in projects:
        try:
            proj = Project.objects.get(pk=p['id'])
        except:
            proj = Project()

        # update properties
        proj.name = p['name']
        proj.description = p['description']
        proj.homepage    = p.get('homepage', '')
        proj.github_url  = p.get('github_url', '')

        if p['organizationId']:
            proj.organization = Organization.objects.get(pk=p['organizationId'])

        # save org before we start modifying its ManyToManyField
        # ref: https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/
        proj.save()
        proj.tags.add(*(saved_tags[tag] for tag in p['tags']))

# load json into database, updating records where needed
fill_auxiliary(Category, saved_categories, organizations, 'categories')
fill_auxiliary(Tag, saved_tags, projects, 'tags')
fill_organizations()
fill_projects()
