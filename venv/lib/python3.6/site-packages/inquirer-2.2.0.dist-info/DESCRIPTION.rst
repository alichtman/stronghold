====================  =================================================================================
Tests                 |travis| |coveralls|
--------------------  ---------------------------------------------------------------------------------
Downloads             |pip dm| |pip dw| |pip dd|
--------------------  ---------------------------------------------------------------------------------
About                 |pip license| |pip wheel| |pip pyversions| |pip implem|
--------------------  ---------------------------------------------------------------------------------
Status                |version| |status|
====================  =================================================================================

Collection of common interactive command line user interfaces, based on `Inquirer.js`_.

Goal and Philosophy
===================

Born as a `Inquirer.js`_ clone, it shares part of the goals and philosophy.

So, **Inquirer** should ease the process of asking end user **questions**, **parsing**, **validating** answers, managing **hierarchical prompts** and providing **error feedback**.

You can `download the python-inquirer code from GitHub`_ or `download the wheel from Pypi`_.


Documentation
=============

Documentation has been moved to `ReadTheDocs`_.

But here you have a couple of usage examples:


Text
----

.. code:: python

  import inquirer
  questions = [
    inquirer.Text('name', message="What's your name"),
    inquirer.Text('surname', message="What's your surname"),
    inquirer.Text('phone', message="What's your phone number",
                  validate=lambda x, _: re.match('\+?\d[\d ]+\d', x),
                  )
  ]
  answers = inquirer.prompt(questions)

|inquirer text|




List
----

Shows a list of choices, and allows the selection of one of them.

Example:

.. code:: python


  import inquirer
  questions = [
    inquirer.List('size',
                  message="What size do you need?",
                  choices=['Jumbo', 'Large', 'Standard', 'Medium', 'Small', 'Micro'],
              ),
  ]
  answers = inquirer.prompt(questions)

List questions can take one extra argument :code:`carousel=False`. If set to true, the answers will rotate (back to first when pressing down on last choice, and down to last choice when pressing up on first choice)

|inquirer list|


Checkbox
--------

Shows a list of choices, with multiple selection.

Example:

.. code:: python


  import inquirer
  questions = [
    inquirer.Checkbox('interests',
                      message="What are you interested in?",
                      choices=['Computers', 'Books', 'Science', 'Nature', 'Fantasy', 'History'],
                      ),
  ]
  answers = inquirer.prompt(questions)

|inquirer checkbox|

License
=======

Copyright (c) 2014 Miguel Ángel García (`@magmax9`_), based on `Inquirer.js`_, by Simon Boudrias (`@vaxilart`_)

Licensed under `the MIT license`_.


.. |travis| image:: https://travis-ci.org/magmax/python-inquirer.png
  :target: `Travis`_
  :alt: Travis results

.. |coveralls| image:: https://coveralls.io/repos/magmax/python-inquirer/badge.png
  :target: `Coveralls`_
  :alt: Coveralls results_

.. |pip version| image:: https://img.shields.io/pypi/v/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Latest PyPI version

.. |pip dm| image:: https://img.shields.io/pypi/dm/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Last month downloads from pypi

.. |pip dw| image:: https://img.shields.io/pypi/dw/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Last week downloads from pypi

.. |pip dd| image:: https://img.shields.io/pypi/dd/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Yesterday downloads from pypi

.. |pip license| image:: https://img.shields.io/pypi/l/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: License

.. |pip wheel| image:: https://img.shields.io/pypi/wheel/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Wheel

.. |pip pyversions| image::  	https://img.shields.io/pypi/pyversions/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Python versions

.. |pip implem| image::  	https://img.shields.io/pypi/implementation/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Python interpreters

.. |status| image::	https://img.shields.io/pypi/status/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Status

.. |version| image:: https://img.shields.io/pypi/v/inquirer.svg
    :target: https://pypi.python.org/pypi/inquirer
    :alt: Status



.. |inquirer text| image:: http://python-inquirer.readthedocs.org/en/latest/_images/inquirer_text.png
  :alt: Example of Text Question

.. |inquirer list| image:: http://python-inquirer.readthedocs.org/en/latest/_images/inquirer_list.png
  :alt: Example of List Question

.. |inquirer checkbox| image:: http://python-inquirer.readthedocs.org/en/latest/_images/inquirer_checkbox.png
  :alt: Example of Checkbox Question

.. _Inquirer.js: https://github.com/SBoudrias/Inquirer.js
.. _Travis: https://travis-ci.org/magmax/python-inquirer
.. _Coveralls: https://coveralls.io/r/magmax/python-inquirer
.. _examples/: https://github.com/magmax/python-inquirer/tree/master/examples
.. _ReadTheDocs: http://python-inquirer.readthedocs.org/
.. _`download the python-inquirer code from GitHub`: https://github.com/magmax/python-inquirer
.. _`download the wheel from Pypi`: https://pypi.python.org/pypi/inquirer

.. _@vaxilart: https://twitter.com/vaxilart
.. _@magmax9: https://twitter.com/magmax9

.. _the MIT license: http://opensource.org/licenses/MIT

.. _changes.rst: https://github.com/magmax/python-inquirer/blob/master/changes.rst


