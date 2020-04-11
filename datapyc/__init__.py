# __init__.py
#
# This file is part of datapyc.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

import sys
from unittest.mock import MagicMock

sys.modules['qutip'] = MagicMock()
sys.modules['lmfit'] = MagicMock()
sys.modules['tqdm'] = MagicMock()
