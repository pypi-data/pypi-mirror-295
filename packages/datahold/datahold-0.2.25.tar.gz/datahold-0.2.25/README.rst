========
datahold
========

Overview
--------

Wrap common mutable datastructures for inheritance with modification.

Content
-------

BaseList
~~~~~~~~

To understand the class ``BaseList`` here the beginning of its code:

.. code-block:: python

    class BaseList:

        data: list

        @functools.wraps(list.__add__)
        def __add__(self, *args, **kwargs):
            data = self.data
            ans = data.__add__(*args, **kwargs)
            self.data = data
            return ans

The following methods are defined this way:
``__add__``, ``__contains__``, ``__delitem__``, ``__eq__``, ``__format__``, ``__ge__``, ``__getitem__``, ``__gt__``, ``__hash__``, ``__iadd__``, ``__imul__``, ``__iter__``, ``__le__``, ``__len__``, ``__lt__``, ``__mul__``, ``__repr__``, ``__reversed__``, ``__rmul__``, ``__setitem__``, ``__str__, append, clear, copy, count, extend, index, insert, pop, remove, reverse, sort``

The only function present in ``list`` and absent in ``BaseList`` is ``__class_getitem__``

We can use ``BaseList`` as parent for a list-like class. It is recommended to implement is the subclass:
- a property named ``data`` with getter and setter wrapping a private variable (for example named ``_data``)
- the ``__init__`` magic method
This allows the creatation of a list-like class with modified behaviour with only minimal effort. To enhance perpormance we can overwrite some of the methods.

OkayList
~~~~~~~~

This class inherits from ``BaseList`` and implements some common sense overwrites for further inheritance. For example:

* the comparison operations are overwritten:
* ``__eq__`` returns ``True`` iff types are equal and data is equal
* ``__ne__`` negates ``__eq__``
* ``__ge__`` returns ``type(self)(other).__le__(self)``
* ``__gt__`` returns ``True`` iff ``__eq__`` returns ``False`` and ``__ge__`` returns ``True``
* ``__lt__`` returns ``True`` iff ``__eq__`` returns ``False`` and ``__le__`` returns ``True``
* ``__le__`` returns ``self.data.__le__(type(self)(other).data)``
* modify ``__eq__`` or ``__le__`` as needed to change the behaviour of the other comparison methods
* ``__hash__`` raises now a more fitting exception
* ``__iadd__`` uses now extend
* ``__init__`` allows now to set data immediately
* see the code for all overwrites

BaseDict
~~~~~~~~

Just like ``BaseList`` but for dict...
The following methods are implemented: ``__contains__``, ``__delitem__``, ``__eq__``, ``__format__``, ``__ge__``, ``__getitem__``, ``__gt__``, ``__hash__``, ``__ior__``, ``__iter__``, ``__le__``, ``__len__``, ``__lt__``, ``__or__``, ``__repr__``, ``__reversed__``, ``__ror__``, ``__setitem__``, ``__str__``, ``clear``, ``copy``, ``get``, ``items``, ``keys``, ``pop``, ``popitem``, ``setdefault``, ``update``, ``values````
The classmethods ``__class_getitem__`` and ``fromkeys`` are not implemented.

BaseSet
~~~~~~~

Just like ``BaseSet`` but for set...
The following methods are implemented: ``__and__``, ``__contains__``, ``__eq__``, ``__format__``, ``__ge__``, ``__gt__``, ``__hash__``, ``__iand__``, ``__ior__``, ``__isub__``, ``__iter__``, ``__ixor__``, ``__le__``, ``__len__``, ``__lt__``, ``__or__``, ``__rand__``, ``__repr__``, ``__ror__``, ``__rsub__``, ``__rxor__``, ``__str__``, ``__sub__``, ``__xor__``, ``add``, ``clear``, ``copy``, ``difference``, ``difference_update``, ``discard``, ``intersection``, ``intersection_update``, ``isdisjoint``, ``issubset``, ``issuperset``, ``pop``, ``remove``, ``symmetric_difference``, ``symmetric_difference_update``, ``union``, ``update``
The classmethod ``__class_getitem__`` is not implemented.

Installation
------------

To install ``datahold``, you can use ``pip``. Open your terminal and run:

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

Thank you for using ``datahold``!