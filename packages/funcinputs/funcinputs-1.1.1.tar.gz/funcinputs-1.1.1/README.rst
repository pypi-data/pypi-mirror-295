==========
funcinputs
==========

Overview
--------

The funcinputs project holds the class FuncInput. The objects of this class represent the entire input that can be passed to a function when the function is called. Each FuncInput object has a list of positional arguments (the property is called `args`) and a dict of keyword arguments (the property is called `kwargs`). One can do everything with a FuncInput object that can be done with a list or a dict e.g. indexers, appending, or updating.

Installation
------------

To install funcinputs, you can use `pip`. Open your terminal and run:

.. code-block:: bash

    pip install funcinputs

Usage
-----

Once funcinputs is installed, you can use it as follows:

.. code-block:: python

    from funcinputs import FuncInput

    x = FuncInput(args=[9, "foo"], kwargs={"bar":12.75})
    print(x) # FuncInput(args=[9, 'foo'], kwargs={'bar': 12.75})
    x += FuncInput(args=[2], kwargs={"baz":"spam"})
    print(x) # FuncInput(args=[9, 'foo', 2], kwargs={'bar': 12.75, 'baz': 'spam'})
    x.append(19)
    print(x) # FuncInput(args=[9, 'foo', 2, 19], kwargs={'bar': 12.75, 'baz': 'spam'})

Features
--------

The class **FuncInput** combines the features of list and dict:

- Properties:

  * ``args``: represents positional arguments in the shape of a list
  * ``kwargs``: represents the keyword-arguments as a dict (the keys must be limited to the type **str**)

- Methods:

  * ``append``: Appends to ``args``
  * ``clear_all``: Combines ``clear_args`` and ``clear_kwargs``
  * ``clear_args``: Clears ``args``
  * ``clear_kwargs``: Clears ``kwargs``
  * ``copy``: Makes a copy
  * ``count``: Counts in ``args``
  * ``exec``: Executes a function and returns the result
  * ``extend``: Extends ``args``
  * ``get``: Gets value from ``kwargs``
  * ``index``: Gets index from ``args``
  * ``insert``: Inserts into ``args``
  * ``items``: Returns ``kwargs.items()`` converted to a list
  * ``keys``: Returns ``kwargs.keys()`` converted to a list
  * ``pop``: Pops value in ``kwargs`` if the key is of the type **str**, otherwise ``args``
  * ``popitem``: Pops item in ``kwargs``
  * ``remove``: Removes from ``args``
  * ``reverse``: Reverses ``args``
  * ``setdefault``: Sets default for ``kwargs``
  * ``sort``: Sorts ``args``
  * ``update``: Updates ``kwargs``
  * ``values``: Returns ``kwargs.values()`` converted to a list

- Other Features:

  * *addition*: Creates a **FuncInput** object from two other objects. The property ``args`` and the property ``kwargs`` are each joined together
  * *indexing*: If the key is of the type **str** then ``kwargs`` is altered in the normal way, otherwise ``args``

License
-------

This project is licensed under the MIT License.

Links
-----

* `Download <https://pypi.org/project/funcinputs/#files>`_
* `Source <https://github.com/johannes-programming/funcinputs>`_

Credits
-------

- Author: Johannes
- Email: johannes-programming@posteo.org

Thank you for using funcinputs!
