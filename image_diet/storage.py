import importlib
from os.path import abspath, basename, dirname, join
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


    def copy_to_temp(self, fullname):
        '''Copy file to the configured temporary directory.

        We can't rely on file's current path to point to directory where
        intermediate files can be created because it might not point to a
        filesystem at all. External tools however are filesystem based so we
        need to process file somewhere safe (configured directory).
        '''
        name = basename(fullname)
        path = join(self.temp_dir, name)
        shutil.copyfile(fullname, path)
        return path

'''
    def save(self, name, content):
        file_content = content.read()
        if self.exists(name):
            self.delete(name)
        f = File(StringIO(file_content))
        return super(DietMixin, self).save(name, File(f))
'''


class DietStorage(DietMixin, STORAGE_CLASS):
    pass
