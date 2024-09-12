===========
na_quantors
===========

Overview
--------

The na_quantors project is a small collection of functions that check arguments for being na-values.

Installation
------------

To install ``na_quantors``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install na_quantors

Implementation
--------------

.. code-block:: python

    import pandas as _pd


    def isna(*values):
        ans = {(_pd.isna(x) is True) for x in values}
        (ans,) = ans
        return ans


    def notna(*values):
        return not isna(*values)


    def allisna(*values):
        return all(isna(x) for x in values)


    def allnotna(*values):
        return all(notna(x) for x in values)


    def anyisna(*values):
        return any(isna(x) for x in values)


    def anynotna(*values):
        return any(notna(x) for x in values)

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/na_quantors>`_
* `Download <https://pypi.org/project/na-quantors/#files>`_
* `Source <https://github.com/johannes-programming/na_quantors>`_

Credits
-------

* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``na_quantors``!