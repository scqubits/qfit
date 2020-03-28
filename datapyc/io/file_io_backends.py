# file_io_backends.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2019, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


from abc import ABC, abstractmethod
import os
import numpy as np
import csv


try:
    import h5py
except ImportError:
    _HAS_H5PY = False
else:
    _HAS_H5PY = True

import datapyc.io.file_io as io


class IOWriter(ABC):
    """
    ABC for writing class instance data to file.

    Parameters
    ----------
    filename: str
    file_handle: h5.Group, optional
    """
    def __init__(self, filename, file_handle=None):
        self.filename = filename
        self.io_data = None
        self.file_handle = file_handle

    @abstractmethod
    def to_file(self, io_data, **kwargs):
        pass

    @abstractmethod
    def write_attributes(self, *args, **kwargs):
        pass

    @abstractmethod
    def write_ndarrays(self, *args, **kwargs):
        pass

    @abstractmethod
    def write_objects(self, *args, **kwargs):
        pass


class H5Writer(IOWriter):
    def write_attributes(self, h5file_group):
        """
        Attribute data consists of those __init__ parameters that are of type str or numerical, and are directly written
        into h5py.attributes

        Parameters
        ----------
        h5file_group: h5py.Group
        """
        h5file_group.attrs.create("__type", self.io_data.typename)    # Record the type of the current class instance
        attributes = self.io_data.attributes
        for attr_name, attr_value in attributes.items():
            if isinstance(attr_value, dict):  # h5py does not serialize dicts automatically, so have to do it manually
                group_name = "__dicts/" + attr_name
                h5file_group.create_group(group_name)
                io.write(attr_value, self.filename, file_handle=h5file_group[group_name])
            elif isinstance(attr_value, (list, tuple)):
                group_name = "__lists/" + attr_name
                h5file_group.create_group(group_name)
                io.write(attr_value, self.filename, file_handle=h5file_group[group_name])
            else:
                h5file_group.attrs[attr_name] = attr_value

    def write_ndarrays(self, h5file_group):
        for name, array in self.io_data.ndarrays.items():
            h5file_group.create_dataset(name, data=array, dtype=array.dtype, compression="gzip")

    def write_objects(self, h5file_group):
        h5file_group = h5file_group.create_group("__objects")
        for obj_name in self.io_data.objects.keys():
            new_h5group = h5file_group.create_group(obj_name)
            io.write(self.io_data.objects[obj_name], self.filename, file_handle=new_h5group)

    def to_file(self, io_data, file_handle=None):
        """
        Takes the serialized IOData and writes it to the given h5py.Group

        Parameters
        ----------
        io_data: IOData
        file_handle: h5py.Group, optional
        """
        self.io_data = io_data
        if file_handle is None:
            h5file_group = h5py.File(self.filename, 'w')
        else:
            h5file_group = file_handle

        self.write_attributes(h5file_group)
        self.write_ndarrays(h5file_group)
        self.write_objects(h5file_group)


class CSVWriter(IOWriter):
    """
    Given filename='somename.csv', write initdata into somename.csv
    Then, additional csv files are written for each dataset, with filenames: 'somename_' + dataname0 + '.csv' etc.
    """
    def append_ndarray_info(self, attributes):
        """Add data set information to attributes, so that dataset names and dimensions are available
        in attributes CSV file."""
        for index, dataname in enumerate(self.io_data.ndarrays.keys()):
            data = self.io_data.ndarrays[dataname]
            attributes['dataset' + str(index)] = dataname

            if data.ndim == 3:
                slice_count = len(data)
            else:
                slice_count = 1
            attributes['dataset' + str(index) + '.slices'] = slice_count
        return attributes

    def write_attributes(self, filename):
        attributes = self.io_data.attributes
        attributes["__type"] = self.io_data.typename
        attributes = self.append_ndarray_info(attributes)
        with open(filename, mode='w', newline='') as meta_file:
            file_writer = csv.writer(meta_file, delimiter=',')
            file_writer.writerow(attributes.keys())
            file_writer.writerow(attributes.values())

    def write_ndarrays(self, filename):
        filename_stub, _ = os.path.splitext(filename)
        for dataname, dataset in self.io_data.ndarrays.items():
            filename = filename_stub + '_' + dataname + '.csv'
            self.write_data(filename, dataset)

    def write_data(self, filename, dataset):
        if dataset.ndim <= 2:
            np.savetxt(filename, dataset)
        else:
            raise Exception("Error: Unexpected array dimensions > 2.")

    def write_objects(self, *args, **kwargs):
        raise NotImplementedError

    def to_file(self, io_data, **kwargs):
        # with open(self.filename, 'ab') as outfile:
        # self.io_data = io_data
        self.write_attributes(self.filename)
        self.write_ndarrays(self.filename)
