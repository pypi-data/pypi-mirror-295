========
scaevola
========

Overview
--------

This project contains the ``Scaevola`` class which can be used as a baseclass to utilize its preset righthanded magic methods: ``__ge__``, ``__gt__``, ``__radd__``, ``__rand__``, ``__rdivmod__``, ``__rfloordiv__``, ``__rlshift__``, ``__rmatmul__``, ``__rmod__``, ``__rmul__``, ``__ror__``, ``__rpow__``, ``__rrshift__``, ``__rsub__``, ``__rtruediv__``, ``__rxor__``


Example
-------

The __radd__ magic method is defined as below. The others follow the same pattern.

.. code-block:: python

    def __radd__(self, other):
        return type(self)(other) + self

Installation
------------

To install ``scaevola``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install scaevola

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/scaevola/#files>`_
* `Source <https://github.com/johannes-programming/scaevola>`_

Credits
-------

- Author: Johannes
- Email: johannes-programming@mailfence.com

Thank you for using ``scaevola``!