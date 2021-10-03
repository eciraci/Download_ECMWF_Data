#!/usr/bin/env python
u"""
download_bbox.py
Written by Enrico Ciraci' (09/2021)

Use the Climate Data Store API to access the ECMWF Reanalysis v5 (ERA5).

Copernicus Data Store Web API are available here:
https://pypi.org/project/cdsapi/

Install CDS AIP using pip: pip install cdsapi

Data download requests can be sent programatically via our API.
However, a user ID and API key must be sent using HTTP basic authentication.
To access ECMWF data Authentication through .cdsapirc id required.
API Key and User ID mu be saved inside a text file named .cdsapirc and saved
inside your home directory.

$ cat ~/.cdsapirc
url: https://cds.climate.copernicus.eu/api/v2
key: <UID>:<API key>
verify: 0

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
    cdsapi: Climate Data Store API -https://cds.climate.copernicus.eu

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
        description="""se the Climate Data Store API to access the
         ECMWF Reanalysis v5 (ERA5).
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
                        help='Domain BBOX - Lon Min,Lat Max,Lat Min,Lon Max')

    parser.add_argument('--shapefile', '-S', type=str, default=None,
                        help='Absolute path the the shapefile containing the'
                             'boundaries of the Region of interest')

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

    # - Python dictionary containing the selected variables as keys
    # - and the relative ECMWF variable code.
    var_dict = {"total_precipitation": "228.128",
                "2_metre_temperature": "167.128",
                "evaporation": "182.128"}

    # - establish connection with ECMWF server
    # server = ECMWFDataServer()
    c = cdsapi.Client()

    # - Import Request Parameters from mars_parameters.yaml
    # with open(os.path.join('.', 'parameters.yaml'), 'r') as y_fid:
    #     req = yaml.safe_load(y_fid)
    # req['area'] = area

    # for var in var_dict.keys():
    #     print('# - Downloading data for:  ' + var)
    #     for year_d in year_seq:
    #         date_seq_str = year_str.replace("1979", str(year_d))
    #         # -
    #         # - update request dictionary
    #         req["date"] = date_seq_str
    #         req["target"] = os.path.join(data_dir,
    #                                      var + '_' + str(year_d) + '.nc')
    #         req["param"] = var_dict[var]
    #         c.retrieve('reanalysis-era5-complete', req,
    #                    var+'_{}.nc'.format(year_d))

    c.retrieve(
        'reanalysis-era5-land-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'variable': [
                '2m_temperature', 'snowfall', 'total_precipitation',
            ],
            'year': [
                '1981'
            ],
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'time': '00:00',
            'area': [
                55, 55, 5,
                135,
            ],
            'format': 'netcdf',
        },
        os.path.join(data_dir, 'era5-request.nc'))


if __name__ == '__main__':
    main()
