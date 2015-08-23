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

# gather all categories/tags, then fill the database with any new ones
def fill_auxiliary(Manager, saved, data, key):
    unsaved = set()

    for d in data:
        unsaved.update(d[key])

    unsaved = unsaved - set(saved.keys())

    for name in unsaved:
        saved[name] = Manager.objects.create(name=name)

# create all groups/projects with the appropriate cats/tags
def fill_organizations():
    for o in organizations:
        # @TODO: WHAT HAPPENS WHEN JSON CHANGES THE NAME OR OTHER DATA? HOW WILL WE KNOW THAT WE HAVE TO UPDATE RATHER THAN INSERT?
        try:
            org = Organization.objects.get(name=o['name'])
        except:
            org = Organization(name=o['name'])

        # update properties
        org.description = o['description'],
        org.homepage    = o.get('homepage', ''),
        org.github_url  = o.get('github_url', '')

        # save org before we start modifying its ManyToManyField
        # ref: https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/
        org.save()

        cats = [saved_categories[cat] for cat in o['categories']]
        org.categories.add(*cats)

def fill_projects():
    for p in projects:
        # @TODO: NAME IS NOT UNIQUE FOR PROJECTS.. WHAT TO DO?
        # @TODO: ALSO... WHAT HAPPENS WHEN JSON CHANGES THE NAME OR OTHER DATA? HOW WILL WE KNOW THAT WE HAVE TO UPDATE RATHER THAN INSERT?
        try:
            proj = Project.objects.get(name=p['name'])
        except:
            proj = Project(name=p['name'])

        # update properties
        proj.description = p['description'],
        proj.homepage    = p.get('homepage', ''),
        proj.github_url  = p.get('github_url', '')

        # save org before we start modifying its ManyToManyField
        # ref: https://docs.djangoproject.com/en/1.8/topics/db/examples/many_to_many/
        proj.save()

        tags = [saved_tags[tag] for tag in p['tags']]
        proj.tags.add(*tags)

fill_auxiliary(Category, saved_categories, organizations, 'categories')
fill_auxiliary(Tag, saved_tags, projects, 'tags')
fill_organizations()
# fill_projects()
