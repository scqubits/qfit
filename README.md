qfit: a tool component of scQubits
==================================

[Tianpu Zhao](https://github.com/ZhaoTianPu), [Danyang Chen](https://github.com/Harrinive), [Jens Koch](https://github.com/jkochNU)

Overview
--------
QFit is your go-to Python application for extracting parameters of superconducting circuits from measured spectroscopy data. Following the four-step workflow, you can get your circuit parameters in no time:

1. **Calibration**: QFit help to establish the mapping from voltage (your experimental tunable input) to circuit parameters (your simulation ingredients). 

2. **Point Extraction**: With just a click, you can locate the peak of the spectrum sweep data with computer-assistance. The extracted date can be simply grouped as a transition and tagged. It even provides filters and plotting parameters for easy data visualization.

3. **Interactive Pre-fit**: See your numerical model result and the data on the same plot for intuitive comparison. Adjust the numerical simulator with simple sliders to get the perfect fit.

4. **Automated Fitting**: With one click, let the numerical optimizers do the work. You can easily configure your fitting: fix or free parameters, set their range, and more.

QFit supports a wide variety of circuit quantum electrodynamic systems, thanks to the powerful Python library `scqubits` as its backend simulator. Once you've extracted your parameters, you can pass them directly to scQubits for any further numerical simulations you need to do.

So, why wait? Dive in and explore what QFit can do for you!

Installation and Usage
----------------------

Install qfit via

    pip install qfit

Once done, you the application can be launched in a python script via

    from qfit import Fit
    Fit(<HilbertSpace>)

where `<HilbertSpace>` is a scqubits HilbertSpace object, the circuit model you want to fit against.

Check out the notebook `Learn_QFit_in_10mins.ipynb` for a quick start guide.

License
-------
[![license](https://img.shields.io/badge/license-New%20BSD-blue.svg)](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)

You are free to use this software, with or without modification, provided that the conditions listed in the LICENSE file
 are satisfied.
 
qfit uses icons from the "Iconic" set by ([P. J. Onori](https://pjonori.com/)), licensed under 
Creative Commons Attribution-ShareAlike 3.0 United States ([CC BY-SA 3.0 US](https://creativecommons.org/licenses/by-sa/3.0/us/)).

The qfit GUI incorporates a range slider widget from the `silx toolkit` library, Copyright (c) European Synchrotron 
Radiation Facility (ESRF). The `silx toolkit` follows the permissive MIT license, requiring inclusion of the subsequent
permissive notice:

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 
