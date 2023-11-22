QFit: Interactive Parameter Fitting for Superconducting Circuits
================================================================

[Tianpu Zhao](https://github.com/ZhaoTianPu), [Danyang Chen](https://github.com/Harrinive), [Jens Koch](https://github.com/jkochNU)

Overview
--------
QFit is your go-to Python application for extracting parameters of superconducting circuits from measured spectroscopy data. Following the four-step workflow, you can get your circuit parameters in no time:

1. **Calibration**: QFit helps to establish the mapping from voltage (your experimental tunable input) to circuit parameters (your simulation ingredients). 

2. **Point Extraction**: With just a click, you can locate the peak of the spectrum sweep data with computer-assistance. The extracted data can be simply grouped as a transition and labeled. QFit even provides filters and coloring options for enhancing data visualization.

3. **Interactive Pre-fit**: See your numerical model result and the data on the same plot for intuitive comparison. Adjust the numerical simulator with simple sliders to improve your fit.

4. **Automated Fitting**: With one click, let the numerical optimizers do the work. You can easily configure your fitting: adjust which paramters are fixed or free, set their range, and more.

QFit supports a wide variety of circuit quantum electrodynamic systems, thanks to the powerful Python library `scqubits` as its backend simulator. Once you've extracted your parameters, you can pass them directly to scQubits for any further numerical simulations you need to do.

So, why wait? Dive in and explore what QFit can do for you!

Installation and Usage
----------------------

Follow these steps to install `QFit`:

1a. Download source code from GitHub (through `Code` button on the top right), unzip the source code folder in a `<directory>`.

OR 

1b. Open a terminal, `cd <directory>` to the directory where you would like to store the source code of `QFit`, then
```
    git clone https://github.com/scqubits/qfit
```
2. (Recommended) Create a virtual environment with python (python >= 3.8 and <= 3.11 is recommended), e.g. run on terminal
```
    conda create -n <env name> python=3.11
    conda activate <env name>
```
3. On terminal, install `QFit` by
```
    cd <directory>/qfit
    conda install --yes --file requirements.txt
    pip install .
```
Once done, the application can be launched in a jupyter notebook session via
```
    from qfit import Fit
    Fit(<HilbertSpace>)
```
where `<HilbertSpace>` is a `scqubits.HilbertSpace` object, the circuit model you want to fit against.

Check out the notebook [QFit_Quick_Start.ipynb](./QFit_Quick_Start.ipynb) for a quick intro tutorial.

License
-------
[![license](https://img.shields.io/badge/license-New%20BSD-blue.svg)](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)

You are free to use this software, with or without modification, provided that the conditions listed in the LICENSE file are satisfied.
 
qfit uses [CoreUI icons]([https://pjonori.com/](https://coreui.io/docs/icons/)), licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions: The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software. 
