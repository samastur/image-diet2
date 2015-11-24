import codecs
import os
import re
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))


'''Next two functions borrowed from pip's setup.py'''
def read(*parts):
    # intentionally *not* adding an encoding option to open
    # see here: https://github.com/pypa/virtualenv/issues/201#issuecomment-3145690
    return codecs.open(os.path.join(HERE, *parts), 'r').read()

def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


long_description = '''\
image-diet2 is a Django application for removing unnecessary bytes from image
files.  It optimizes images without changing their look or visual quality
("losslessly").

DEFINITELY NOT READY FOR PRODUCTION USE YET!

It works on images in JPEG, GIF, PNG or any format with configured a
processing pipeline. Integration with Django's storage system provides a
seamless integration with most thumbnailing apps.'''

setup(
    author="Marko Samastur",
    author_email="markos@gaivo.net",
    name='image-diet2',
    version=find_version('image_diet', '__init__.py'),
    description='Remove unnecessary bytes from images',
    long_description=long_description,
    url='https://github.com/samastur/image-diet2/',
    platforms=['OS Independent'],
    license='MIT License',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
        'Topic :: Utilities',
    ],
    install_requires=[
        'Django>=1.6',
        'importlib~=1.0.3',
        'pyimagediet>=0.9',
    ],
    include_package_data=True,
    packages=['image_diet'],
    zip_safe=False
)
