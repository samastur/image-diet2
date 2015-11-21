import importlib
from io import BytesIO
import os
from os.path import abspath, basename, dirname, join, exists
import shutil

from django.conf import settings
from django.core.files.base import File
import pyimagediet as diet


THIS_DIR = abspath(dirname(__file__))

DEFAULT_STORAGE = 'django.core.files.storage.FileSystemStorage'
STORAGE_MODULE, STORAGE_CLASSNAME = getattr(
    settings, 'DIET_STORAGE', DEFAULT_STORAGE).rsplit('.', 1)

storage_module = importlib.import_module(STORAGE_MODULE)
STORAGE_CLASS = getattr(storage_module, STORAGE_CLASSNAME)

CUSTOM_CONFIG = getattr(settings, 'DIET_CONFIG', '')


class DietMixin(object):
    def __init__(self, *args, **kwargs):
        default_config = join(THIS_DIR, 'default.yml')

        config = diet.read_yaml_configuration(default_config)
        diet.update_configuration(config,
                                  diet.read_yaml_configuration(CUSTOM_CONFIG))
        self.config = config
        self.temp_dir = self.config.get('tempdir', '/tmp')


    def save_to_temp(self, fullname, content):
        name = basename(fullname)
        path = join(self.temp_dir, name)
        with open(path, 'wb') as f:
            f.write(content)
        return path

    def _save(self, name, content):
        file_content = content.read()
        tmppath = ""

        try:
            tmppath = self.save_to_temp(name, file_content)
            changed = diet.diet(tmppath, self.config)
            if changed:  # pragma: no branch
                # If changed, then tmppath points to compressed contents.
                with open(tmppath, 'rb') as f:
                    file_content = f.read() # pragma: no branch

            f = File(BytesIO(file_content))
        finally:
            # Always clean up after ourselves
            os.remove(tmppath)
        return super(DietMixin, self)._save(name, File(f))


class DietStorage(DietMixin, STORAGE_CLASS):
    pass
