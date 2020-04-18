Source for datapyc documentation
===================================

This directory contains the source files for the datapyc documentation.


Build requirements
------------------

* Sphinx: http://sphinx-doc.org/  version 2.2+
* sphinx_rtd_theme
* numpydoc
* nbsphinx

In a conda environment use:
    
    $ conda install -c conda-forge sphinx
    $ conda install numpydoc sphinx_rtd_theme
    $ conda install -c conda-forge nbsphinx

Build
-----

    > make html
