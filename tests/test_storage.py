import filecmp
import os
from os.path import abspath, dirname, join, exists
import pytest

from image_diet import storage


THIS_DIR = abspath(dirname(__file__))


@pytest.fixture
def dietstorage():
    dietstorage = storage.DietStorage()
    # Filesystem storage parameters
    dietstorage.location = THIS_DIR
    dietstorage.file_permissions_mode = 0o644
    return dietstorage


def test_the_right_storage_has_been_imported():
    from django.core import files

    assert files.storage.FileSystemStorage == storage.STORAGE_CLASS


def test_get_configuration_returns_parsed_configuration():
    config = storage.get_configuration()

    assert config['commands']['fake'] == 'fakecmd'
    assert config['commands']['advpng'] == 'advpng'


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


def test_save_to_temp_copies_content_to_same_named_file_in_temp_directory():
    mixin = storage.DietMixin()

    filename = 'stockholm.jpg'
    path = join(THIS_DIR, 'test_files', 'stockholm.jpg')
    with open(path, 'rb') as f:
        content = f.read()

    tmppath = join(mixin.temp_dir, filename)

    try:
        assert not exists(tmppath)
        assert mixin.save_to_temp(path, content) == tmppath
        assert exists(tmppath)
        assert filecmp.cmp(path, tmppath)

    finally:
        os.remove(tmppath)


def test_save_method_saves_text_file(dietstorage):
    filename = 'tempfile.txt'
    content = "This file is empty."
    path = join(THIS_DIR, filename)

    tmppath = join(dietstorage.temp_dir, filename)
    tmppath = dietstorage.save_to_temp(path, content)

    new_path = dietstorage._save(path, open(tmppath, 'r'))

    try:
        assert exists(new_path)
        assert open(new_path, 'r').read() == content
        assert not exists(tmppath)
    finally:
        os.remove(new_path)


def test_save_method_saves_binary_file(dietstorage):
    filename = 'stockholm.jpg'
    path = join(THIS_DIR, 'test_files', 'stockholm.jpg')
    with open(path, 'rb') as f:
        content = f.read()

    tmppath = join(dietstorage.temp_dir, filename)
    tmppath = dietstorage.save_to_temp(path, content)

    new_path = dietstorage._save(path, open(tmppath, 'rb'))

    try:
        assert exists(new_path)
        assert open(new_path, 'rb').read() == content
        assert not exists(tmppath)
    finally:
        os.remove(new_path)


def test_save_method_compresses(dietstorage):
    filename = 'png_test.png'
    path = join(THIS_DIR, 'test_files', 'png_test.png')
    with open(path, 'rb') as f:
        content = f.read()

    tmppath = join(dietstorage.temp_dir, filename)
    tmppath = dietstorage.save_to_temp(path, content)

    new_path = dietstorage._save(path, open(tmppath, 'rb'))

    try:
        assert exists(new_path)
        assert len(open(new_path, 'rb').read()) < len(content)
        assert not exists(tmppath)
    finally:
        os.remove(new_path)


def test_logger_logs_errors(caplog, dietstorage):
    # Delete configuration section so that DietException will be raised
    del dietstorage.config['commands']

    filename = 'stockholm.jpg'
    path = join(THIS_DIR, 'test_files', 'stockholm.jpg')

    tmppath = join(dietstorage.temp_dir, filename)

    try:
        dietstorage._save(path, open(path, 'rb'))
    except storage.diet.DietException as e:
        assert not exists(tmppath)
        assert isinstance(e, storage.diet.ConfigurationErrorDietException)

    records = list(caplog.records())
    assert len(records) == 1
    record = records[0]
    assert record.levelname == 'ERROR'
    assert record.message.startswith('Missing key(s) in configuration: ')


def test_save_method_cleans_temp_directory(dietstorage):
    filename = 'stockholm.jpg'
    path = join(THIS_DIR, 'test_files', 'stockholm.jpg')

    tmppath = join(dietstorage.temp_dir, filename)
    new_path = dietstorage._save(path, open(path, 'rb'))

    try:
        assert not exists(tmppath)
    finally:
        os.remove(new_path)
