.. datapyc
   Copyright (C) 2020, Jens Koch

.. _dataformats:

**********************
Supported Data Formats
**********************

datapyc aims to support file formats commonly used in experimental labs. The currently supported data formats are:

.. csv-table:: supported file/data formats
   :header: "file type", "origin", "comments"
   :widths: 20, 30, 60

   ".h5, .hdf5", "generic hdf5 file", "datapyc uses heuristics to identify stored arrays of floats likely to represent measurement data"
   ".h5, .hdf5", "Labber", "Based on the hierarchical file structure used by Labber 1.7, datapyc attempts to extract relevant measurement data"
   ".mat", "Matlab", "MAT file format used by Matlab for array storage. datapyc relies on ``scipy.io.loadmat`` for reading .mat files."
   ".csv", "generic CSV data", "Comma Separated Value data is read using ``numpy.loadtxt``."