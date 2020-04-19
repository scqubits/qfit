.. datapyc
   Copyright (C)  2020, Jens Koch

.. _guide:

*******************
Users Guide
*******************

.. toctree::
   :maxdepth: 2



.. _run:

Running datapyc
====================

Following installation, datapyc is started from the command line like this:

.. code-block:: bash

   python -m datapyc


.. _import:

Data import
====================

Once launched, datapyc displays a dialog window for selecting a data file to be opened.
As a concrete example, such data might represent a spectroscopy scan recording
the transmission amplitude (the stored z-axis data) as a function of probe frequency (x axis) and magnetic flux (y axis).

The list of supported file formats includes Labber, Matlab, generic hdf5 files, as well as common image file formats.
See :ref:`dataformats` for details.


.. _main:

Interface
===========

Once measurement data has been imported, it is displayed in the main window. The graphical interface consists of several
elements:

.. figure:: ../graphics/main-window.jpg
   :align: center
   :width: 7.5in


.. _tools:

Tool/mode selection
---------------------

The group of four buttons on the top lets the user switch between selection, zoom, and pan mode, reset the data view,
and swap the x- and y-axes. (Swapping axes is enabled for numerical measurement data, but is disabled for data imported
from images/)

.. figure:: ../graphics/tools.jpg
   :align: center
   :width: 3.5in

Selection mode is used for selecting data point by simple point & click on the displayed measurement data.



.. _selectdata:

Measurement data selection
-----------------------------

If the opened data file contains multiple data sets, then the dropdown menus shown below enable switching between the
different data sets.

.. figure:: ../graphics/data-select.jpg
   :align: center
   :width: 2.5in