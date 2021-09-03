dwdGrilbExtractor: A tiny Python interface to request and extract NWP grib file data from opendata.dwd.de
========================================================================================================

.. image:: https://img.shields.io/pypi/v/cfgrib.svg
   :target: https://pypi.python.org/pypi/cfgrib/

dwdGribExtractor is a smart package to easely extract data from `numerical weather prediction <https://www.dwd.de/EN/ourservices/nwp_forecast_data/nwp_forecast_data.html>`_ 
grib files provided by DWD.
The difference to other packages is the location flexibility. So every point
on the 2.2km x 2.2km grid (ICON-D2) can be retrieved for the next X forecast hours.    

At the moment only ICON_D2 is supported.

Supported weather variables
===========================
For currently available weather variabels see: `ICON Database <https://www.dwd.de/DWD/forschung/nwv/fepub/icon_database_main.pdf/>`_
Chapter 6.1.3 table 6.3

Installation
============
To read the grib2 files `xarray <http://xarray.pydata.org/en/stable/>`_ with `cfgrib <https://github.com/ecmwf/cfgrib/>`_ engine is used. 
The easiest way to install *cfgrib* and all its binary dependencies is via `Conda <https://conda.io/>`_::

    $ conda install -c conda-forge cfgrib

alternatively, if you install the binary dependencies yourself, you can install the
Python package from *PyPI* with::

    $ pip install cfgrib

Binary dependencies
-------------------

*cfgrib* depends on the `eccodes python package <https://pypi.org/project/eccodes>`_
to access the ECMWF *ecCodes* binary library,
when not using *conda* please follow the *System dependencies* section there.

Windows
-------
It is strongly recommended to use Unix enironment running *dwdGrib2location*. For 
windows several issues my appear. At the moment *dwdGrib2location* is tested
with Windows10 and works if following requirements are satiesfied.
To build eccodes on windows by your own should be avoided. The easiest way to 
use eccodes on windows is to install it in an `MSYS <https://www.msys2.org/>`_ environment. 

1. Install MSYS

2. Install `eccodes <https://packages.msys2.org/base/mingw-w64-eccodes>`_. Depending on your system run in the MSYS cli::

    $ pacman -S mingw-w64-ucrt-x86_64-eccodes

3. Set environment variables::

    ECCODES_DIR = <path_to_ecccodes_install_dir> e.g (C:\msys64\ucrt64)
    ECCODES_DEFINITION_PATH = <path_to_eccodes_definitions> (e.g C:\msys64\ucrt64\share\eccodes\definitions)

4. Add eccodes to path. This is the folder inside the MSYS environment where the .exe files are located::

    e.g. C:\msys64\ucrt64\bin  

5. Install ecCodes::

    $ pip install eccodes

6. Install cfgrib::

    $ pip install cfgrib

7. Check if cfgrib is working::

    $ python -m cfgrib selfcheck
    Found: ecCodes v2.20.0.
    Your system is ready.

Linux
-----
1) Install eccodes with apt or `build it by your own <https://gist.github.com/MHBalsmeier/a01ad4e07ecf467c90fad2ac7719844a>`_
TODO

License
=======

Code license
------------
Licensed under the MIT license. See `LICENSE <https://github.com/panodata/dwdGrib2location/blob/master/LICENSE>`_ for details.

Data license
------------
The DWD has information about their terms of use policy in
`German <https://www.dwd.de/DE/service/copyright/copyright_node.html>`_
and
`English <https://www.dwd.de/EN/service/copyright/copyright_node.html>`_.
