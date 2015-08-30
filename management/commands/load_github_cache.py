from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Loads GitHub cache data into the database from a named file.'

    def add_arguments(self, parser):
        parser.add_argument('filename',
            metavar='FILE',
            help='The fixture you want to load data from.',
            type=str)

    def handle(self, *args, **options):
        try:
            infile = options['filename']
            call_command('loaddata',
                '--app', 'search', infile)
        except:
            raise CommandError('Unable to load GitHub cache data from file.')
