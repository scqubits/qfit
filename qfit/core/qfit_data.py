# qfit_data.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################


import qfit.io_utils.file_io_serializers as serializers

from qfit.calibration.calibration_data import CalibrationData

serializers.SERIALIZABLE_REGISTRY["CalibrationData"] = CalibrationData


class QfitData(serializers.Serializable):
    def __init__(
        self,
        datanames,
        datalist,
        z_data=None,
        x_data=None,
        y_data=None,
        image_data=None,
        calibration_data=None,
        tag_data=None,
        fit_results=None,
    ):
        """
        Class for fitting experimental spectroscopy data to the Hamiltonian model of the qubit / coupled quantum system.

        Parameters
        ----------
        datanames: list of str
        datalist: list of ndarray
            Each ndarray has float entries and is of the form array([[x1,y1], [x2,y2], ...]). Each such set corresponds
            to data extracted from experimental spectroscopy data. Each corresponds to one particular transition among
            dressed-level eigenstates.
        z_data: ndarray
        x_data: ndarray
        y_data: ndarray
        image_data: ndarray
            as obtained with matplotlib.image.imread
        calibration_data: qfit.CalibrationData
        """
        super().__init__()
        self.datanames = datanames
        self.datalist = datalist
        self.x_data = x_data
        self.y_data = y_data
        self.z_data = z_data
        self.image_data = image_data
        self.calibration_data = calibration_data
        self.tag_data = tag_data
        self.fit_results = fit_results

        self.system = None
        self.subsys_names = None
        self.sweep_name = None
        self.sweep_vals = None
        self.update_func = None
        self.sweep_update_func = None
        self.subsys_update_list = None
        self.params = None
        self.fit_params = {}
        self.evals_count = None
        self.sweep = None
        self.transitions = None
