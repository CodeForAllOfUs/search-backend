import argparse

from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Dumps GitHub cache data to stdout.'

    def add_arguments(self, parser):
        # parser.add_argument('--save',
        #     default=self.stdout,
        #     type=argparse.FileType('w'))
        pass

    def handle(self, *args, **options):
        try:
            # outfile = options['save']
            call_command('dumpdata',
                'search.GitHubOrganizationCache',
                'search.GitHubProjectCache',
                # GitHubProjectCache depends on ProgrammingLanguage
                'search.ProgrammingLanguage',
                '--indent', '4')
        except:
            raise CommandError('Unable to dump GitHub cache data.')
