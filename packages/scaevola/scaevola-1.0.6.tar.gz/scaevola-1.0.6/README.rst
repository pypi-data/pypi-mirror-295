========
scaevola
========

Overview
--------

This project contains the Scaevola class which can be used as a baseclass. Scaevola has preset righthanded magic methods.

Example
-------

The __radd__ magic method is defined as below. The others follow the same pattern.

.. code-block:: python

    def __radd__(self, other):
        return type(self)(other) + self


Installation
------------

To install scaevola, you can use `pip`. Open your terminal and run:

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

Thank you for using scaevola!