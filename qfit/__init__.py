# __init__.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import scqubits as scq
from qfit.core.qfit import Fit
from qfit.version import __version__, __version_tuple__

scq.settings.PROGRESSBAR_DISABLED = True



