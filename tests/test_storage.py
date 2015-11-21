import filecmp
import os
from os.path import abspath, basename, dirname, join, exists
from image_diet import storage


THIS_DIR = abspath(dirname(__file__))


def test_the_right_storage_has_been_imported():
    from django.core import files

    assert files.storage.FileSystemStorage == storage.STORAGE_CLASS


def test_mixin_reads_default_configuration():
    mixin = storage.DietMixin()

    assert hasattr(mixin, 'config')
    assert mixin.config['commands']['optipng'] == 'optipng'
    assert mixin.temp_dir == '/tmp'


def test_mixin_also_reads_custom_configuration():
    mixin = storage.DietMixin()

    assert mixin.config['commands']['optipng'] == 'optipng'
    assert mixin.config['commands']['fake'] == 'fakecmd'
    assert mixin.config['notreal'] == 'not a real value'


def test_copy_to_temp_makes_a_copy_in_temp_directory():
    mixin = storage.DietMixin()

    filename = 'tempfile.txt'
    content = "This file is empty."

    path = join(THIS_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)

    tmppath = join(mixin.temp_dir, filename)
    assert not exists(tmppath)

    assert mixin.copy_to_temp(path) == tmppath
    assert exists(tmppath)
    assert filecmp.cmp(path, tmppath)

    os.remove(path)
    os.remove(tmppath)
