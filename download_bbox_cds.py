#!/usr/bin/env python
u"""
download_bbox_cds.py
Written by Enrico Ciraci' (09/2021)

Use the Climate Data Store API to access the ECMWF Reanalysis v5 (ERA5).

Copernicus Data Store Web API are available here:
https://pypi.org/project/cdsapi/

How to use the API:
https://cds.climate.copernicus.eu/api-how-to

Install CDS AIP using pip: pip install cdsapi

Data download requests can be sent programmatically via our API.
However, a user ID and API key must be sent using HTTP basic authentication.
To access ECMWF data Authentication through .cdsapirc id required.
API Key and User ID mu be saved inside a text file named .cdsapirc and saved
inside your home directory.

$ cat ~/.cdsapirc
url: https://cds.climate.copernicus.eu/api/v2
key: <UID>:<API key>
verify: 0

API request general structure:
import cdsapi
c = cdsapi.Client()

c.retrieve("dataset-short-name",
           {... sub-selection request ...},
           "target-file")

NOTE: API request parameters are provided in the form of JSON document saved in
     -> csd_parameters.json

COMMAND LINE OPTIONS:
  -h, --help            show this help message and exit
  --path PATH, -P PATH  Absolute Output Path.
  --directory DIRECTORY, -D DIRECTORY
                        Output data directory name.
  --boundaries BOUNDARIES, -B BOUNDARIES
                        Domain BBOX - Lon Min,Lat Max,Lat Min,Lon Max
  --name NAME, -N NAME  Dataset Short Name
  --shapefile SHAPEFILE, -S SHAPEFILE
                        Absolute path the the shapefile containing
                        the boundaries of the Region of interest


PYTHON DEPENDENCIES:
    argparse: Parser for command-line options, arguments and sub-commands
           https://docs.python.org/3/library/argparse.html
    numpy: The fundamental package for scientific computing with Python
           https://numpy.org/
    json:  JSON encoder and decoder.
           https://docs.python.org/3/library/json.html
    cdsapi: Climate Data Store API
           https://cds.climate.copernicus.eu
    datetime: Basic date and time types
           https://docs.python.org/3/library/datetime.html

UPDATE HISTORY:
"""
# - - python dependencies
from __future__ import print_function
import os
import sys
import argparse
import geopandas as gpd
import numpy as np
import cdsapi
import json
from datetime import datetime


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
        description="""Use the Climate Data Store API to access the
         ECMWF Reanalysis v5 (ERA5).
        """
    )
    #
    parser.add_argument('--path', '-P', type=str, default=None,
                        help='Absolute Output Path.')

    parser.add_argument('--directory', '-D', type=str, default=None,
                        help='Output data directory name.')

    parser.add_argument('--boundaries', '-B', type=str, default=None,
                        help='Domain BBOX - Lon Min,Lat Max,Lat Min,Lon Max')

    parser.add_argument('--name', '-N', type=str, default=None,
                        help='Dataset Short Name')

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

    if not args.name:
        print('# - Provide dataset short name.')
        sys.exit()

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
    area = [str(lat_max), str(lon_min), str(lat_min), str(lon_max)]

    # - establish connection with Climate Data Store server
    c = cdsapi.Client()

    # - Import Request Parameters from cds_parameters.json
    with open(os.path.join('.', 'cds_parameters.json'), 'r') as j_fid:
        req = json.loads(j_fid.read())
    req['area'] = area

    today_date = datetime.today().strftime('%Y-%m-%d')
    c.retrieve(args.name, req,
               os.path.join(data_dir, '{}_{}.nc'.format(args.name, today_date)))


if __name__ == '__main__':
    main()
