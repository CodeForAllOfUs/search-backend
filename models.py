import json
from django.db import models
from django.utils import timezone

class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class GitHubCache(models.Model):
    github_path = models.CharField(max_length=255, unique=True, blank=False, null=False)
    fetched = models.DateTimeField('time fetched', default=timezone.now)
    json = models.TextField()

    def toJSON(self):
        return {
            'github_path': self.github_path,
            'data': json.loads(self.json),
        }

    def __str__(self):
        return self.github_path

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    homepage = models.URLField(max_length=255)
    github_path = models.CharField(max_length=255, unique=True, null=True)
    github_data = models.ForeignKey(GitHubCache, null=True)
    categories = models.ManyToManyField(Category)

    # Override save method to allow `github_path` to be unique and NULL (not present)
    # ref https://docs.djangoproject.com/en/1.8/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.github_path = self.github_path or None
        super(Organization, self).save(*args, **kwargs)

    def toJSON(self):
        ret = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'homepage': self.homepage,
            'categories': [cat.name for cat in self.categories.all()],
        }

        if self.github_path:
            ret['github_path'] = self.github_path

        return ret

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    homepage = models.URLField(max_length=255)
    github_path = models.CharField(max_length=255, unique=True, null=True)
    github_data = models.ForeignKey(GitHubCache, null=True)
    organization = models.ForeignKey(Organization, null=True)
    tags = models.ManyToManyField(Tag)

    # Override save method to allow `github_path` to be unique and NULL (not present)
    # ref https://docs.djangoproject.com/en/1.8/topics/db/models/#overriding-model-methods
    def save(self, *args, **kwargs):
        self.github_path = self.github_path or None
        super(Project, self).save(*args, **kwargs)

    def toJSON(self):
        ret = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'homepage': self.homepage,
            'tags': [tag.name for tag in self.tags.all()],
        }

        if self.github_path:
            ret['github_path'] = self.github_path

        if self.organization:
            ret['organizationId'] = self.organization.id

        return ret

    def __str__(self):
        return self.name
