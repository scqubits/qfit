# appstate.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

from enum import Enum, auto, unique


@unique
class State(Enum):
    SELECT = auto()
    ZOOM = auto()
    PAN = auto()
    CALIBRATE_X1 = auto()
    CALIBRATE_X2 = auto()
    CALIBRATE_Y1 = auto()
    CALIBRATE_Y2 = auto()


state = State.SELECT
