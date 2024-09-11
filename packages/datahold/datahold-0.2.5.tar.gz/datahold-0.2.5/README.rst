========
datahold
========

Overview
--------

Wrap common datastructures for inheritance with modification.

Explanation
-----------

.. code-block:: python

    class BaseList:

        data: list

        @functools.wraps(list.__add__)
        def __add__(self, *args, **kwargs):
            data = self.data
            ans = data.__add__(*args, **kwargs)
            self.data = data
            return ans

        # The following functions are defined the same way:
        # __contains__, __delitem__, __eq__, __format__, __ge__, __getitem__, __gt__, __hash__, __iadd__, __imul__, __iter__, __le__, __len__, __lt__, __mul__, __reduce__, __reduce_ex__, __repr__, __reversed__, __rmul__, __setitem__, __str__,
        # append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort

Installation
------------

To install datahold, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install datahold

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/datahold/#files>`_
* `Source <https://github.com/johannes-programming/datahold>`_

Credits
-------

- Author: Johannes
- Email: johannes-programming@mailfence.com

Thank you for using datahold!