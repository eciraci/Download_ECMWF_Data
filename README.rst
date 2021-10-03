=======================================
Download Reanalysis Data from ECMWF
=======================================
|Language|
|License|

.. |Language| image:: https://img.shields.io/badge/python-v3.7-green.svg
   :target: https://www.python.org/

.. |License| image:: https://img.shields.io/badge/license-MIT-green.svg
   :target: https://github.com/eciraci/Download_ECMWF_Data/blob/main/LICENSE

A collection of scripts to download reanalysis data distributed by the
European Centre for Medium-Range Weather Forecasts - ECMWF through:
1. Meteorological Archival and Retrieval System (MARS) API.
2. Climate Data Store - Copernicus API.

The MARS API can be used to access old generation of ECMWF public datasets like
ERA-Interim. A complete list of the datasets available through this
interface is reported here:
https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets

The CDS API can be used to download all the datasets belonging to the
ECMWF Reanalysis v5 (ERA5).


**PYTHON DEPENDENCIES**:
 - `ecmwfapi: enables you to programmatically request and retrieve data via HTTP from the ECMWF data archive <https://www.ecmwf.int>`_
 - `cdsapi: Climate Data Store API <https://cds.climate.copernicus.eu>`_
 - `PyYaml: full-featured YAML framework for the Python programming language <https://pyyaml.org>`_
 - `json: JSON encoder and decoder <https://docs.python.org/3/library/json.html>`_
 - `numpy: The fundamental package for scientific computing with Python <https://numpy.org>`_


License
#######

The content of this project is licensed under the
`Creative Commons Attribution 4.0 Attribution license <https://creativecommons.org/licenses/by/4.0/>`_
and the source code is licensed under the `MIT license <LICENSE>`_.
