.. _quickstart:


Quickstart
==========

Configuration
-------------

After you have installed image-diet package and external compression tools,
you need to configure it.

First, you need to point image-diet to your configuration file which you do
by adding ``DIET_CONFIG`` setting to your project's settings. Its value is the
absolute path to the configuration file you want to use.

Configuration is stored in YAML format and is described in
:ref:`pyimagediet's documentation <pyimagediet:configure>` (image-diet2 uses
pyimagediet for actual processing).

An additional value you can set in image-diet2's configuration file  is
``tmpdir`` that should point to directory where temporary files will be created.
Its default value is ``/tmp``.

If you are using filesystem (Django's default) as storage and would like to
process files with image-diet2 everywhere it is used, then add to settings::

    DEFAULT_FILE_STORAGE = 'image_diet.storage.DietStorage'

If you are using some other backend class that you would like to augment with
``DietStorage``, then set ``DIET_STORAGE`` setting to that storage class.


Default values
--------------

image-diet2 already comes with some default values so you do not have to know
or type everything. It is enough to provide only changes you want to make and
they will either replace previous ones or be added if they are new.

Default configuration file:

.. literalinclude:: ../image_diet/default.yml


DietMixin
---------

In case your project uses different storage backends or want to use compression
only on non-default storage backend then you should use
``image_diet.storage.DietMixin`` mixin.
