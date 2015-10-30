from django.db import models
from django.utils import timezone

class NamedAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

class Category(NamedAttribute):
    class Meta:
        verbose_name_plural = 'categories'

class Tag(NamedAttribute): pass
class ProgrammingLanguage(NamedAttribute): pass
class License(NamedAttribute): pass

class GitHubCache(models.Model):
    github_path = models.CharField(max_length=255, unique=True, blank=False, null=False, db_index=True)
    fetched = models.DateTimeField('time fetched', default=timezone.now)
    json = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.github_path

class GitHubOrganizationCache(GitHubCache):
    def toJSON(self):
        return {
            'github_path': self.github_path,
        }

class GitHubProjectCache(GitHubCache):
    open_issues_count = models.IntegerField(db_index=True)
    stargazers_count = models.IntegerField(db_index=True)
    last_commit = models.DateTimeField('last commit date', null=True, db_index=True)
    language = models.ForeignKey(ProgrammingLanguage, null=True)

    class Meta:
        get_latest_by = 'last_commit'

    def toJSON(self):
        return {
            'github_path': self.github_path,
            'open_issues_count': self.open_issues_count,
            'stargazers_count': self.stargazers_count,
            'last_commit': self.last_commit,
            'language': self.language.name if self.language else None,
        }

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    homepage = models.URLField(max_length=255)
    categories = models.ManyToManyField(Category)
    # @TODO: this is data duplication with github_data.github_path
    github_path = models.CharField(max_length=255, unique=True, blank=False, null=True)
    github_data = models.ForeignKey(GitHubOrganizationCache, null=True)

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
    license = models.ForeignKey(License)
    organization = models.ForeignKey(Organization, null=True)
    tags = models.ManyToManyField(Tag)
    # @TODO: this is data duplication with github_data.github_path
    github_path = models.CharField(max_length=255, unique=True, blank=False, null=True)
    github_data = models.ForeignKey(GitHubProjectCache, null=True)

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
            'license': self.license.name,
            'tags': [tag.name for tag in self.tags.all()],
        }

        if self.github_path:
            ret['github_path'] = self.github_path

        if self.organization:
            ret['organizationId'] = self.organization.id

        return ret

    def __str__(self):
        return self.name
