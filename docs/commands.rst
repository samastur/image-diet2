.. _commands:


Management commands
===================

image-diet2 comes with management commands to make your life a bit easier.


check_diet_tools
----------------

This command will check system for most common compression tools and print
paths of those found in format ready for inclusion in YAML configuration file.

You can also use command line utility `diet` that comes with pyimagediet which
was installed together with image-diet2. You can read about how to use it in
:ref:`pyimagediet's documentation <pyimagediet:tools>`


diet_images
-----------

This command will traverse provided list of directories and compress all files
with matching pipeline according to image-diet2's configuration.
