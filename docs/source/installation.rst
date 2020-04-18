.. datapyc
   Copyright (C)  2020, Jens Koch

.. _install:

**************
Installation
**************

datapyc runs under Python 3.6, 3.7, and 3.8. The package, including its dependencies, can be installed as follows.

.. _install-via_conda:

Installing via conda
====================

When using the Anaconda Python distribution, datapyc can be installed through the `conda` package manager:

.. code-block:: bash

   conda install -c conda-forge datapyc



.. _install-via_pip:

Installing via pip
==================

datapyc can also be installed using the Python package manager `pip <http://www.pip-installer.org/>`_.

.. code-block:: bash

   pip install datapyc




.. _install-requires:

General Requirements
=====================

datapyc depends on the following Python open-source libraries, installed automatically with datapyc when using
one of the above install methods:


.. cssclass:: table-striped

+----------------+--------------+-----------------------------------------------------+
| Package        | Version      | Details                                             |
+================+==============+=====================================================+
| **Python**     | 3.6+         | Version 3.6 and higher is supported.                |
+----------------+--------------+-----------------------------------------------------+
| **NumPy**      | 1.14.2+      | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **SciPy**      | 1.1.0+       | Not tested on lower versions.                       |
+----------------+--------------+-----------------------------------------------------+
| **Matplotlib** | 3.0.0+       | Some plotting does not work on lower versions.      |
+----------------+--------------+-----------------------------------------------------+
| **PySide2**    | 5.14+        | GUI                                                 |
+----------------+--------------+-----------------------------------------------------+
| **h5py**       | 2.7.1+       | Read/write h5 files                                 |
+----------------+--------------+-----------------------------------------------------+

