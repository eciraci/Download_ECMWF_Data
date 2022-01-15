#!/usr/bin/env python
u"""
download_bbox.py
Written by Enrico Ciraci' (09/2021)

Use the ECMWF Web API to access the Meteorological  Archival and Retrieval
System to access/download data from ECMWF's operational and other archives,
including the online Fields Data Base (FDB).

A complete list of the datasets available through this interface can be found
here:
https://confluence.ecmwf.int/display/WEBAPI/Available+ECMWF+Public+Datasets

Several examples of available queries can be found here:
https://confluence.ecmwf.int/display/WEBAPI/Python+ERA-interim+examples

List of available variables and equivalent parameters:
https://apps.ecmwf.int/codes/grib/param-db

More details about the MARS interface and on how to use the ECMWF Web API
are available here: https://apps.ecmwf.int/

ECMWF Web API:
https://www.ecmwf.int/en/forecasts/access-forecasts/access-archive-datasets

MARS Interface:
https://confluence.ecmwf.int/display/UDOC/MARS+user+documentation

- ECMWF Data Access Website:
- https://www.ecmwf.int/en/forecasts/datasets/archive-datasets

- ECMWF WEB API service:
  https://github.com/ecmwf/ecmwf-api-client
  https://www.ecmwf.int/en/forecasts/access-forecasts/ecmwf-web-api

- Prerequisites:
   - An ECMWF account (determines which data you can receive)
   - An ECMWF API key (you need to be logged in to access this URL)
   - Access to the internet

-  API Setup Instructions: <<- IMPORTANT
-  https://confluence.ecmwf.int/display/WEBAPI/Access+ECMWF+Public+Datasets
-
-  Install Python API using pip:
   Install via pip with:  pip install ecmwf-api-client

- ECMWF WEB API website + examples:
  https://confluence.ecmwf.int/display/WEBAPI/Python+ERA-interim+examples

- List of the available dataset from ECMWF:
- https://apps.ecmwf.int/datasets/

COMMAND LINE OPTIONS:

  -h, --help            show this help message and exit
  --path PATH, -P PATH  Absolute Output Path.
  --directory DIRECTORY, -D DIRECTORY
                        Output data directory name.
  --f_year F_YEAR, -F F_YEAR
                        First year of the considered period.
  --l_year L_YEAR, -L L_YEAR
                        Last year of the considered period.
  --boundaries BOUNDARIES, -B BOUNDARIES
                        Domain BBOX - Lon Min,Lat Max,Lat Min,Lon Max
  --shapefile SHAPEFILE, -S SHAPEFILE
                        Absolute path the the shapefile containing
                        the boundaries of the Region of interest


PYTHON DEPENDENCIES:
    argparse: Parser for command-line options, arguments and sub-commands
           https://docs.python.org/3/library/argparse.html
    numpy: The fundamental package for scientific computing with Python
           https://numpy.org/
    PyYaml:full-featured YAML framework for the Python programming language.
           https://pyyaml.org/
    ecmwfapi: enables you to programmatically request and retrieve data
           via HTTP from the ECMWF data archive - https://www.ecmwf.int

UPDATE HISTORY:
"""
# - - python dependencies
from __future__ import print_function
import os
import sys
import argparse
from ecmwfapi import ECMWFDataServer
import geopandas as gpd
import numpy as np
import yaml


def create_dir(abs_path: str, dir_name: str) -> str:
    """
    Create directory
    :param abs_path: absolute path to the output directory
    :param dir_name: new directory name
    :return: absolute path to the new directory
    """
    import os
    dir_to_create = os.path.join(abs_path, dir_name)
    if not os.path.exists(dir_to_create):
        os.mkdir(dir_to_create)
    return dir_to_create


def main():
    # - Read the system arguments listed after the program
    parser = argparse.ArgumentParser(
        description="""Use the ECMWF Web API to access the Meteorological 
        Archival and Retrieval System to access/download data from ECMWF's 
        operational and other archives, including the online Fields Data Base 
        (FDB).
        """
    )
    #
    parser.add_argument('--path', '-P', type=str, default=None,
                        help='Absolute Output Path.')

    parser.add_argument('--directory', '-D', type=str, default=None,
                        help='Output data directory name.')

    parser.add_argument('--f_year', '-F', type=int, default=1979,
                        help='First year of the considered period.')

    parser.add_argument('--l_year', '-L', type=int, default=2020,
                        help='Last year of the considered period.')

    parser.add_argument('--boundaries', '-B', type=str, default=None,
                        help='Domain BBOX - Lat Min,Lat Max,Lon Min,Lon Max')

    parser.add_argument('--shapefile', '-S', type=str, default=None,
                        help='Absolute path the the shapefile containing the'
                             ' boundaries of the Region of interest')

    args = parser.parse_args()

    # -
    if not os.path.exists(args.path):
        print('# - Selected Output Path Not Found.')
        sys.exit()
    else:
        data_dir = create_dir(args.path, args.directory)

    if not args.boundaries and not args.shapefile:
        print('# - Provide Region of interest boundaries/bbox. See Options:')
        print('# - --boundaries, -B : Domain BBOX - '
              'Lon Min,Lat Max,Lat Min,Lon Max')
        print('#-  --boundaries, -B : Domain BBOX - Lon Min,Lat '
              'Max,Lat Min,Lon Max')
        sys.exit()

    # - Import Data Domain Boundaries
    lat_min = None
    lat_max = None
    lon_min = None
    lon_max = None

    if args.boundaries is not None:
        bound_list = args.boundaries.split(',')
        lat_min = bound_list[0]
        lat_max = bound_list[1]
        lon_min = bound_list[2]
        lon_max = bound_list[3]

    if args.shapefile is not None:
        gdf = gpd.read_file(args.shapefile)
        gdf_bounds = gdf.bounds
        lat_min = float(np.min([gdf_bounds['miny'], gdf_bounds['maxy']]))
        lat_max = float(np.max([gdf_bounds['miny'], gdf_bounds['maxy']]))
        lon_min = float(np.min([gdf_bounds['minx'], gdf_bounds['maxx']]))
        lon_max = float(np.max([gdf_bounds['minx'], gdf_bounds['maxx']]))

    # - Selected Data Domain
    area = '{}/{}/{}/{}'.format(lat_min, lon_min, lat_max, lon_max)

    # - list of years of data to download
    year_seq = range(args.f_year, args.l_year+1)
    # - year_reference string
    year_str = "19790101/19790201/19790301/19790401/19790501/19790601" \
               "/19790701/19790801/19790901/19791001/19791101/19791201"

    # - establish connection with ECMWF server
    server = ECMWFDataServer()

    # - Import Request Parameters from mars_parameters.yaml
    with open(os.path.join('.', 'mars_parameters.yaml'), 'r') as y_fid:
        req = yaml.safe_load(y_fid)
    req['area'] = area

    print('# - Downloading Selected Data.')
    for year_d in year_seq:
        date_seq_str = year_str.replace("1979", str(year_d))

        # - update request dictionary
        req["date"] = date_seq_str
        req["target"] = os.path.join(data_dir,
                                     req["name"] + '_' + str(year_d) + '.nc')
        server.retrieve(req)


if __name__ == '__main__':
    main()
