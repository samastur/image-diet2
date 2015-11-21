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


def create_file(filename, content):
    path = join(THIS_DIR, filename)
    with open(path, 'w') as f:
        f.write(content)
    return path


def test_save_to_temp_copies_content_to_same_named_file_in_temp_directory():
    mixin = storage.DietMixin()

    filename = 'tempfile.txt'
    content = "This file is empty."
    path = create_file(filename, content)

    tmppath = join(mixin.temp_dir, filename)
    assert not exists(tmppath)

    assert mixin.save_to_temp(path, content) == tmppath
    assert exists(tmppath)
    assert filecmp.cmp(path, tmppath)

    os.remove(path)
    os.remove(tmppath)


def test_save_method_saves_file():
    dietstorage = storage.DietStorage()

    filename = 'tempfile.txt'
    content = "This file is empty."
    path = join(THIS_DIR, filename)

    # Filesystem storage parameters
    dietstorage.location = THIS_DIR
    dietstorage.file_permissions_mode = 0o644

    tmppath = join(dietstorage.temp_dir, filename)
    tmppath = dietstorage.save_to_temp(path, content)

    new_path = dietstorage._save(path, open(tmppath, 'rb'))

    assert exists(new_path)
    assert open(new_path, 'r').read() == content
    assert not exists(tmppath)
    os.remove(new_path)



def test_save_method_cleans_temp_directory():
    dietstorage = storage.DietStorage()

    filename = 'tempfile.txt'
    content = "This file is empty."
    path = create_file(filename, content)

    # Filesystem storage parameters
    dietstorage.location = THIS_DIR
    dietstorage.file_permissions_mode = 0o644

    tmppath = join(dietstorage.temp_dir, filename)
    new_path = dietstorage._save(path, open(path, 'rb'))

    assert not exists(tmppath)
    os.remove(path)
    os.remove(new_path)
