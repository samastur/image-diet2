from setuptools import setup

long_description = '''\
image-diet2 is a Django application for removing unnecessary bytes from image
files.  It optimizes images without changing their look or visual quality
("losslessly").

It works on images in JPEG, GIF and PNG formats and will leave others
unchanged. Provides a seemless integration with easy_thumbnails app, but can
work with others too.'''

setup(
    author="Marko Samastur",
    author_email="markos@gaivo.net",
    name='image-diet2',
    version='0.7.1',
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
        'pyimagediet>=0.5',
    ],
    include_package_data=True,
    packages=['image_diet'],
    zip_safe=False
)
