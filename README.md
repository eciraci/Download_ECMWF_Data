# Download Reanalysis Data from ECMWF

[![Language][]][1] [![License][]][2]

A collection of scripts to download reanalysis data distributed by the
European Centre for Medium-Range Weather Forecasts - ECMWF through: 1.
Meteorological Archival and Retrieval System (MARS) API. 2. Climate Data
Store - Copernicus API.

The MARS API can be used to access old generation of ECMWF public
datasets like ERA-Interim. A complete list of the datasets available
through this interface is reported here:
<https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets>

The CDS API can be used to download all the datasets belonging to the
ECMWF Reanalysis v5 (ERA5).

**Installation**:

1.  Setup minimal **conda** installation using [Miniconda][]

2.  Create Python Virtual Environment

    > -   Creating an environment with commands ([Link][]);
    > -   Creating an environment from an environment.yml file
    >     ([Link][3]);

3.  Install Python Dependencies

    > ``` bash
    > conda install -c conda-forge ecmwf-api-client 
    > ```


**PYTHON DEPENDENCIES**:  
-   [ecmwfapi: enables you to programmatically request and retrieve data
    via HTTP from the ECMWF data archive][]
-   [cdsapi: Climate Data Store API][]
-   [PyYaml: full-featured YAML framework for the Python programming
    language][]
-   [json: JSON encoder and decoder][]
-   [numpy: The fundamental package for scientific computing with
    Python][]

## License

The content of this project is licensed under the [Creative Commons
Attribution 4.0 Attribution license][] and the source code is licensed
under the [MIT license][].

  [Language]: https://img.shields.io/badge/python-3.7%2B-green.svg
  [1]: https://www.python.org/
  [License]: https://img.shields.io/badge/license-MIT-green.svg
  [2]: https://github.com/eciraci/Download_ECMWF_Data/blob/main/LICENSE
  [ecmwfapi: enables you to programmatically request and retrieve data via HTTP from the ECMWF data archive]:
    https://www.ecmwf.int
  [cdsapi: Climate Data Store API]: https://cds.climate.copernicus.eu
  [PyYaml: full-featured YAML framework for the Python programming language]:
    https://pyyaml.org
  [json: JSON encoder and decoder]: https://docs.python.org/3/library/json.html
  [numpy: The fundamental package for scientific computing with Python]:
    https://numpy.org
  [Creative Commons Attribution 4.0 Attribution license]: https://creativecommons.org/licenses/by/4.0/
  [MIT license]: LICENSE

  [Miniconda]: https://docs.conda.io/en/latest/miniconda.html
  [Link]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-with-commands
  [3]: https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file