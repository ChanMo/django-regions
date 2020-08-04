from django.core.management.base import BaseCommand, CommandError
from regions.models import Region

class Command(BaseCommand):
    help = 'Sync regions data from amap api'

    def handle(self, *args, **options):
        try:
            Region.objects.sync()
        except Exception as e:
            raise CommandError(e)
        self.stdout.write(self.style.SUCCESS('done.'))
