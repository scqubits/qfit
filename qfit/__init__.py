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
__all__ = [
    "Fit",
    "__version__",
    "__version_tuple__",
]

from qfit.core.qfit import Fit
from qfit.version import __version__, __version_tuple__
import qfit.settings as _settings
from qfit.utils.helpers import executed_in_ipython as _executed_in_ipython

if _executed_in_ipython():
    # inside ipython, the function get_ipython is always in globals()
    ipython = get_ipython()
    ipython.run_line_magic("gui", "qt6")
    _settings.EXECUTED_IN_IPYTHON = True
else:
    _settings.EXECUTED_IN_IPYTHON = False

# scqubits settings
import scqubits as _scq
import scqubits.utils.plotting as _scq_plotting
_scq.settings.PROGRESSBAR_DISABLED = True
_scq.settings.MULTIPROC = "pathos"
_scq.settings.FUZZY_SLICING = True
_scq.settings.FUZZY_WARNING = False
# disable default label lines in scqubits
_scq_plotting._LABELLINES_ENABLED = False

