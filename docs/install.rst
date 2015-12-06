.. _install:

Installation
============

This part of the documentation covers the installation of image-diet2.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing image-diet2 is simple with `pip <https://pip.pypa.io>`_, just run
this in your terminal::

    $ pip install image-diet2

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install image-diet2

But, you really `shouldn't do that <https://stackoverflow.com/questions/3220404/why-use-pip-over-easy-install>`_.


Get the Code
------------

image-diet2 is developed on GitHub, where the code is
`always available <https://github.com/samastur/image-diet2>`_.

You can either clone the public repository::

    $ git clone git://github.com/samastur/image-diet2.git

Download the `tarball <https://github.com/samastur/image-diet2/tarball/master>`_::

    $ curl -OL https://github.com/samastur/image-diet2/tarball/master

Or, download the `zipball <https://github.com/samastur/image-diet2/zipball/master>`_::

    $ curl -OL https://github.com/samastur/image-diet2/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install


Installing "dependencies"
-------------------------

image-diet2 does not have a hard dependency on any external optimisation tool,
but it also does not do anything useful without any. You do need to install at
least one for each image format you want to handle.

You can find a list of some in :ref:`pyimagediet's documentation <pyimagediet:exttools>`.
