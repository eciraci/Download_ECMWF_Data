# Download Reanalysis Data from ECMWF
A collection of scripts to download reanalysis data  distributed by the 
European Centre for Medium-Range Weather Forecasts - ECMWF through:
1. Meteorological Archival and Retrieval System (MARS) API.
2. Climate Data Store API.

The MARS API can be used to access old generation of ECMWF public datasets like
ERA-Interim. A complete list of the datasets available through this 
interface is reported here:
https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets

The CDS API can be used to download all the datasets belonging to the 
ECMWF Reanalysis v5 (ERA5).


**PYTHON DEPENDENCIES**:
 - *ecmwfapi*: enables you to programmatically request and retrieve data
           via HTTP from the ECMWF data archive - https://www.ecmwf.int
 - *cdsapi*: Climate Data Store API -https://cds.climate.copernicus.eu

 - *PyYaml*:full-featured YAML framework for the Python programming language.
           https://pyyaml.org
 -  - *numpy*: The fundamental package for scientific computing with Python
           https://numpy.org
