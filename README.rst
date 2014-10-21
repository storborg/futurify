Futurify - Manage your __future__ statements
============================================

Scott Torborg - `Cart Logic <http://www.cartlogic.com>`_

``futurify`` is a simple tool for managing forward-compatible
``from __future__ import...`` statements in your Python projects.


Installation
============

Install with pip::

    $ pip install futurify


Example Usage
=============

Add some future statements to a file tree::

    $ futurify +absolute_import +print_function myproject/

Add some, remove others::

    $ futurify -print_function +division myproject/


API Usage
=========

.. code-block:: python

    import futurify

    futurify.process_tree('myproject',
                          add=['absolute_import', 'print_function'])

    futurify.process_file('hello.py',
                          add=['absolute_import'],
                          remove=['division'])


License
=======

Futurify is released under the MIT license. See ``LICENSE`` for details.
