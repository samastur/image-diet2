import os
from os.path import join
from django.core.management.base import BaseCommand
import pyimagediet

from ...storage import get_configuration


class Command(BaseCommand):
    args = '<dir1> [<dir2>...]'
    help = "Scan directories and subdirectories for images and compress them."

    @staticmethod
    def get_files(*input_dirs):
        for dirname in input_dirs:
            for (root, dirs, files) in os.walk(dirname):
                for filename in files:
                    yield join(root, filename)

    def handle(self, *args, **options):
        config = get_configuration()
        for filename in self.get_files(*args):
            self.stdout.write('Processing: {0}\n'.format(filename))
            pyimagediet.diet(filename, config)
