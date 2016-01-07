from django.core.management.base import BaseCommand
from pyimagediet.helpers import get_config


class Command(BaseCommand):
    help = ("Check which popular external compression tools are "
            "available and suggest commands section configuration.")

    def handle(self, *args, **options):
        self.stdout.write(get_config())
        self.stdout.write("\n")
