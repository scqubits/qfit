# qfit_app.py
#
# This file is part of qfit.
#
#    Copyright (c) 2020, Jens Koch
#    All rights reserved.
#
#    This source code is licensed under the BSD-style license found in the
#    LICENSE file in the root directory of this source tree.
############################################################################

if __name__ == "__main__":

    import scqubits as scq
    from qfit import Fit

    # just a test for now
    resonator = scq.Oscillator(
        E_osc = 3,
        l_osc = 1.0,
        truncated_dim = 4,
        id_str = "resonator"
    )
        
    fluxonium = scq.Fluxonium(
        EJ = 7.0,
        EC = 1,
        EL = 0.2,
        flux = 0.0,
        cutoff = 100,
        truncated_dim = 5,
        id_str = "fluxonium"
    )

    hilbertspace = scq.HilbertSpace([resonator, fluxonium])

    hilbertspace.add_interaction(
        g = 1,
        op1 = resonator.n_operator,
        op2 = fluxonium.n_operator,
        add_hc = False,
        id_str = "res-qubit"
    )

    qfit_app = Fit(hilbertspace)
    # qfit_app = Fit.new(hilbertspace)
    # Fit.open("./../example_data/test.qfit")

