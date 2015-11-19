import importlib
from os.path import abspath, dirname, join

from django.conf import settings
from django.core.files.base import File
import pyimagediet.diet as diet


THIS_DIR = abspath(dirname(__file__))

DEFAULT_STORAGE = 'django.core.files.storage.FileSystemStorage'
STORAGE_MODULE, STORAGE_CLASSNAME = getattr(
    settings, 'DIET_STORAGE', DEFAULT_STORAGE).rsplit('.', 1)

storage_module = importlib.import_module(STORAGE_MODULE)
STORAGE_CLASS = getattr(storage_module, STORAGE_CLASSNAME)

CUSTOM_CONFIG = getattr(settings, 'DIET_CONFIG', '')


def update_config(orig, new):
    dicts = ('commands', 'parameters', 'pipelines')
    for key in dicts:
        if key in new:
            orig[key].update(new[key])

    for key in new:
        if key not in dicts:
            orig[key] = new[key]


class DietMixin(object):
    def __init__(self, *args, **kwargs):
        default_config = join(THIS_DIR, 'default.yml')

        config = diet.read_yaml_configuration(default_config)
        update_config(config, diet.read_yaml_configuration(CUSTOM_CONFIG))
        self.config = config

'''
    def save(self, name, content):
        file_content = content.read()
        if self.exists(name):
            self.delete(name)
        f = File(StringIO(file_content))
        return super(DietMixin, self).save(name, File(f))


class DietStorage(DietMixin, STORAGE_CLASS):
    pass
'''
