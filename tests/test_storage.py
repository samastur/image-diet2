from image_diet import storage


def test_the_right_storage_has_been_imported():
    from django.core import files

    assert files.storage.FileSystemStorage == storage.STORAGE_CLASS


def test_mixin_reads_default_configuration():
    mixin = storage.DietMixin()

    assert hasattr(mixin, 'config')
    assert mixin.config['commands']['optipng'] == 'optipng'


def test_mixin_also_reads_custom_configuration():
    mixin = storage.DietMixin()

    assert mixin.config['commands']['optipng'] == 'optipng'
    assert mixin.config['commands']['fake'] == 'fakecmd'
    assert mixin.config['notreal'] == 'not a real value'
