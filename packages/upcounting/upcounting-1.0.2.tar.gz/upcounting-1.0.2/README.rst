==========
upcounting
==========

Overview
--------

Counts until condition. Infinite counting is also supported.

Installation
------------

To install ``upcounting``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install upcounting

Implementation
--------------

.. code-block:: python

    def count_up(start=0, stop=None, step=1):
        ans = start
        while True:
            if stop is None:
                pass
            elif callable(stop):
                if stop(ans):
                    break
            else:
                if ans >= stop:
                    break
            yield ans
            ans += step

License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/upcounting>`_
* `Download <https://pypi.org/project/upcounting/#files>`_
* `Source <https://github.com/johannes-programming/upcounting>`_

Credits
-------

* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``upcounting``!