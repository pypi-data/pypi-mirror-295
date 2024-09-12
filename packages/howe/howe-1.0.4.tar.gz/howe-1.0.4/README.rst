====
howe
====

Overview
--------

The ``howe`` project contains the ``Howe`` class. A ``Howe`` object is similar to a ``zip`` object, except that all the iterators have to run out at the same time. Otherwise an ``ExceptionGroup`` (containing the ``StopIteration`` exceptions from the iterators that did run out) will be raised. The project is named for E. Howe, one of the intentors of the zipper.

Installation
------------

To install ``howe``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install howe

Implementation
--------------

.. code-block:: python

    class Howe:
        def __init__(self, *args):
            self._args = [iter(x) for x in args]

        def __iter__(self):
            return self

        def __next__(self):
            elements = list()
            errors = list()
            for arg in self._args:
                try:
                    element = next(arg)
                except StopIteration as error:
                    errors.append(error)
                else:
                    elements.append(element)
            if not len(errors):
                return tuple(elements)
            if len(elements):
                raise ExceptionGroup("Howe failed.", errors)
            raise StopIteration

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/howe>`_
* `Download <https://pypi.org/project/howe/#files>`_
* `Source <https://github.com/johannes-programming/howe>`_

Credits
-------

* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``howe``!