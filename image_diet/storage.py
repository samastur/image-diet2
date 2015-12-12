import importlib
from io import BytesIO, StringIO
import os
from os.path import abspath, basename, dirname, join

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


def get_configuration():
    default_config = join(THIS_DIR, 'default.yml')

    config = diet.read_yaml_configuration(default_config)
    diet.update_configuration(config,
                              diet.read_yaml_configuration(CUSTOM_CONFIG))
    return config


class DietMixin(object):
    def __init__(self, *args, **kwargs):
        self.config = get_configuration()
        self.temp_dir = self.config.get('tempdir', '/tmp')
        super(DietMixin, self).__init__(*args, **kwargs)

    def save_to_temp(self, fullname, content):
        name = basename(fullname)
        path = join(self.temp_dir, name)
        mode = 'wb' if type(content) == bytes else 'wt'
        with open(path, mode) as f:
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
                    file_content = f.read()  # pragma: no branch

            f = File(BytesIO(file_content))
        # TypeError is for catching different handling of text in Python3
        except TypeError:  # pragma: no branch
            f = File(StringIO(file_content))
        finally:
            # Always clean up after ourselves
            os.remove(tmppath)
        return super(DietMixin, self)._save(name, File(f))


class DietStorage(DietMixin, STORAGE_CLASS):
    pass
