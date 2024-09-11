========
datahold
========

Overview
--------

Wrap common datastructures for inheritance with modification.

Content
-------

BaseList
~~~~~~~~

To understand the class BaseList here the beginning of its code:

.. code-block:: python

    class BaseList:

        data: list

        @functools.wraps(list.__add__)
        def __add__(self, *args, **kwargs):
            data = self.data
            ans = data.__add__(*args, **kwargs)
            self.data = data
            return ans

The following functions are defined the same way:
__contains__, __delitem__, __eq__, __format__, __ge__, __getitem__, __gt__, __hash__, __iadd__, __imul__, __iter__, __le__, __len__, __lt__, __mul__, __reduce__, __reduce_ex__, __repr__, __reversed__, __rmul__, __setitem__, __str__, append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort

The only function preset in list and absent in BaseList is __class_getitem__

We can use BaseList as parent for a list-like class. It is recommended to implement is the subclass:
- a property named data with getter and setter wrapping a private variable (for example named _data)
- the __init__ magic method
This allows the creatation of a list-like class with modified behaviour with only minimal effort. To enhance perpormance we can overwrite some of the methods.

OkayList
~~~~~~~~

This class inherits from BaseList and implements some common sense overwrites for further inheritance. For example:
* the comparison operations are overwritten:
* __eq__ returns True iff types are equal and data is equal
* __ne__ negates __eq__
* __ge__ returns type(self)(other).__le__(self)
* __gt__ returns True iff __eq__ returns False and __ge__ returns True
* __lt__ returns True iff __eq__ returns False and __le__ returns True
* __le__ returns self.data.__le__(type(self)(other).data)
* modify __eq__ or __le__ as needed to change the behaviour of the other comparison methods
* __hash__ raises now a more fitting exception
* __iadd__ uses now extend
* __init__ allows now to set data immediately
* see the code for all overwrites

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