# calibrationmodel.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import numpy as np
from datapyc.io.file_io_serializers import Serializable


class CalibrationModel(Serializable):
    def __init__(self, rawVec1=None, rawVec2=None, mapVec1=None, mapVec2=None):
        self.rawVec1 = rawVec1
        self.rawVec2 = rawVec2
        self.mapVec1 = mapVec1
        self.mapVec2 = mapVec2
        self.bVec = None
        self.alphaMat = None
        self.setCalibration((1., 0.), (0., 1.), (1., 0.), (0., 1.))
        self.applyCalibration = False
        self.msg = None

    def toggleCalibration(self):
        self.applyCalibration = not self.applyCalibration

    def setCalibration(self, rawVec1, rawVec2, mapVec1, mapVec2):
        x1, y1 = rawVec1
        x2, y2 = rawVec2
        x1p, y1p = mapVec1
        x2p, y2p = mapVec2

        # if (x1 == x2) or (y1 == y2):
        #     self.view.calibrationErrorMsg()
        #     return

        alphaX = (x1p - x2p) / (x1 - x2)
        alphaY = (y1p - y2p) / (y1 - y2)

        self.bVec = np.asarray([x1p - alphaX * x1, y1p - alphaY * y1])
        self.alphaMat = np.asarray([[alphaX, 0.], [0., alphaY]])
        self.rawVec1, self.rawVec2, self.mapVec1, self.mapVec2 = rawVec1, rawVec2, mapVec1, mapVec2

    def conversionFunc(self):
        def identityFunc(rowVec):
            return rowVec

        def convFunc(rawVec):
            rVec = np.asarray(rawVec)
            mVec = np.matmul(self.alphaMat, rVec) + self.bVec
            return mVec.tolist()

        if not self.applyCalibration:
            return identityFunc
        return convFunc
