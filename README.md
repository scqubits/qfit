QFit: Interactive Parameter Fitting for Superconducting Circuits
================================================================

[<img src="https://github.com/scqubits/qfit/assets/68950614/514cc57c-675d-4aee-b902-0dda7ab14213" width="100">](https://designawards.core77.com/2024/Apps-Platforms.html)
[![Anaconda-Server Badge](https://anaconda.org/conda-forge/qfit/badges/version.svg)](https://anaconda.org/conda-forge/qfit) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/qfit/badges/downloads.svg)](https://anaconda.org/conda-forge/qfit) [![Anaconda-Server Badge](https://anaconda.org/conda-forge/qfit/badges/latest_release_date.svg)](https://anaconda.org/conda-forge/qfit)

**Notice: This package is currently in beta testing. Bugs and issues are expected. We greatly appreciate your feedback and bug reports to help us improve.**

Developers: [Tianpu Zhao](https://github.com/ZhaoTianPu), [Danyang Chen](https://github.com/Harrinive), [Jens Koch](https://github.com/jkochNU)

UI/UX designer: [Tianying Lyu](https://tianyinglyu.com)

Overview
--------
QFit is your go-to Python application for extracting parameters of superconducting circuits from measured spectroscopy data. Following the four-step workflow, you can get your circuit parameters in no time:

1. **Calibration**: QFit helps to establish the mapping from voltage (your experimental tunable input) to circuit parameters (your simulation ingredients). 

2. **Point Extraction**: With just a click, you can locate the peak of the spectrum sweep data with computer-assistance. The extracted data can be simply grouped as a transition and labeled. QFit even provides filters and coloring options for enhancing data visualization.

3. **Interactive Pre-fit**: See your numerical model result and the data on the same plot for intuitive comparison. Adjust the numerical simulator with simple sliders to improve your fit.

4. **Automated Fitting**: With one click, let the numerical optimizers do the work. You can easily configure your fitting: adjust which paramters are fixed or free, set their range, and more.

QFit supports a wide variety of circuit quantum electrodynamic systems, thanks to the powerful Python library `scqubits` as its backend simulator. Once you've extracted your parameters, you can pass them directly to scQubits for any further numerical simulations you need to do.

Join us in refining QFit during its beta phase! Your insights and reports are invaluable in making QFit a robust tool for this community. Dive in and explore what QFit can do for you, and let us know your experience!

Installation and Usage
----------------------

Follow these steps to install `QFit`:

1. (Optional but highly Recommended) Create a virtual environment with python (version > 3.10). If you are using conda, run on terminal
```
    conda create -n <env name> python=3.10
    conda activate <env name>
```
2. On terminal, install `QFit` by
```
    conda install conda-forge::qfit
```
Once done, the application can be launched in a jupyter notebook session via
```
    from qfit import Fit
    Fit(<HilbertSpace>)
```
where `<HilbertSpace>` is a `scqubits.HilbertSpace` object, the circuit model you want to fit against.

Check out the notebook [QFit_Quick_Start.ipynb](./QFit_Quick_Start.ipynb) for a quick intro tutorial, and [QFit_Advanced_Tips.ipynb](./QFit_Advanced_Tips.ipynb) for further information.

> [!NOTE]
> While you can install QFit with 
> ```pip install qfit```
> this may cause crashes on recent macOS versions due to compatibility issues with pip-installed scipy. As a workaround, you can run `conda install scipy` afterward, though using conda for the full installation is preferred.

License
-------
[![license](https://img.shields.io/badge/license-New%20BSD-blue.svg)](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)

You are free to use this software, with or without modification, provided that the conditions listed in the LICENSE file are satisfied.

qfit uses Qt library under license [GNU Lesser General Public License v3.0](https://www.gnu.org/licenses/lgpl-3.0.html).
 
qfit uses [CoreUI icons](https://coreui.io/docs/icons/) and [Font Awesome icons](https://fontawesome.com/icons) licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), and [SVG Reop icons](https://www.svgrepo.com) licensed under the MIT license.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 
