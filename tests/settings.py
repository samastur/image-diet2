from os.path import abspath, dirname, join

SETTINGS_DIR = abspath(dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

DIET_CONFIG = join(SETTINGS_DIR, 'config.yml')

SECRET_KEY = 'tests'

INSTALLED_APPS = (
    'tests',
)
