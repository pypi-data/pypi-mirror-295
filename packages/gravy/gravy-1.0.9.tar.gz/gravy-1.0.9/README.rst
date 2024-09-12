=====
gravy
=====

Overview
--------

Calculate the GRAVY score of a amino acid sequence.

Installation
------------

To install ``gravy``, you can use ``pip``. Open your terminal and run:

.. code-block:: bash

    pip install gravy

Usage
-----

CLI
~~~

.. code-block:: bash

    python3 -m gravy CYIQNCPLG
    # output: 0.33333
    # the formatting can be change with the option '--format'

Python
~~~~~~

.. code-block:: python

    import gravy
    x = gravy.score("CYIQNCPLG")
    y = format(x, ".5f")
    print(y)
    # output: 0.33333
    # the same format as the default in the CLI


License
-------

This project is licensed under the MIT License.

Links
-----

* `Documentation <https://pypi.org/project/gravy>`_
* `Download <https://pypi.org/project/gravy/#files>`_
* `Source <https://github.com/johannes-programming/gravy>`_

Credits
-------

* Author: Johannes
* Email: johannes-programming@mailfence.com

Thank you for using ``gravy``!