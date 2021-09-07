dwdGribExtractor: A tiny Python interface to request and extract NWP grib file data from opendata.dwd.de
========================================================================================================

.. image:: https://img.shields.io/pypi/v/dwdGribExtractor.svg
   :target: https://img.shields.io/pypi/v/dwdGribExtractor

dwdGribExtractor is a smart package to easely extract data from `numerical weather prediction <https://www.dwd.de/EN/ourservices/nwp_forecast_data/nwp_forecast_data.html>`_ 
grib files provided by DWD.
The difference to other packages is the location flexibility. So every point
on the 2.2km x 2.2km grid (ICON-D2) can be retrieved for the next X forecast hours.    

At the moment only ICON_D2 is supported.

Supported weather variables
===========================
For currently available weather variabels see: `ICON User Manual <https://www.dwd.de/SharedDocs/downloads/DE/modelldokumentationen/nwv/icon/icon_dbbeschr_aktuell.pdf?view=nasPublication&nn=495490/>`_
Chapter 6.1.4 table 6.4

Installation
============
Install with pip::

    $ pip install dwdGrilbExtractor
    
Dependencies
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
windows several issues may appear. At the moment *dwdGrib2location* is tested
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
1. Install eccodes with apt or `build it by your own <https://gist.github.com/MHBalsmeier/a01ad4e07ecf467c90fad2ac7719844a>`_
TODO

Example
============
.. code-block:: python

    locationList = {     
        "Vienna": {
            "lat": 48.20,
            "lon": 16.37     
        },
        "Graz": {
            "lat": 47.07,
            "lon": 15.43     
        }
    }
    
    variables = ["aswdir_s", "aswdifd_s", "t_2m"]
    
    forecast = ICON_D2(locations = locationList, forecastHours = 3)
    data = forecast.collectData(varList = variables, cores = None) # Disable multiprocessing
    #data = forecast.collectData(varList = variables, cores = 4)
    
    
    #### Indexing one location
    loc = "Graz"
    result = data.loc[loc]
    result = data.loc[loc, "2021-09-06 06:15:00"]

    #### Indexing multiple locations
    loc = ["Graz", "Vienna"]
    result = data.loc[loc]
    
    #### Indexing one location with datetime condition
    loc = "Graz"
    mask = data.loc[loc].index.get_level_values(0) > np.datetime64('2021-09-06T06:15:00')
    mask = data.loc[loc].index.get_level_values(0).hour == 8
    result = data.loc[loc][mask]
    
    #### Indexing multiple locations with datetime condition
    loc = ["Graz", "Vienna"]
    mask = data.loc[loc].index.get_level_values(1) > np.datetime64('2021-09-06 06:15:00')
    mask = data.loc[loc].index.get_level_values(1).hour == 8
    result = data.loc[loc][mask]
    
Knwon Issues
============
Windows
-------
- Multiprocessing on some windows machines may not work. Disable it by setting ``forecast.collectData(varList = variables, cores = None)`` 
- `Spyder IDE <https://www.spyder-ide.org/>`_ does not produce print outputs if multiprocessing is enabled.
- Dont run the code in Spyder with F5 or debug mode. This calls runfile() and sometimes crashes memory.  

Author
======
Manuel Strohmaier

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
