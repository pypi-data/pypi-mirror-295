# -*- coding: utf-8 -*-
"""
Utility functions.
"""
import os
import io
import numpy as np
import pathlib
import smart_open
import smart_open.http as so_http
from time import sleep
import concurrent.futures
# import importlib
from copy import copy

from . import v202401
# import v202401

so_http.DEFAULT_BUFFER_SIZE = 524288

#########################################
### parameters

file_dict = {
             'rec_tags.blt': 'https://b2.tethys-ts.xyz/file/nz-mfe/nps-fm-2020/rec_tags.blt',
             'lake_tags.blt': 'https://b2.tethys-ts.xyz/file/nz-mfe/nps-fm-2020/lake_tags.blt',
             }


########################################
### Functions


def calc_stat(ts_data, stat, percentile_method='hazen'):
    """

    """
    if stat == 'median':
        value = ts_data.median()
    elif stat == 'max':
        value = ts_data.max()
    elif 'Q' in stat:
        percentile = int(stat[1:])
        value = np.percentile(ts_data, percentile, method=percentile_method)
    elif 'G' in stat:
        conc = int(stat[1:])
        value = (ts_data > conc).sum()

    return value


def calc_stats(ts_data, limits):
    """

    """
    stats = {stat: calc_stat(ts_data, stat) for stat in limits['A']}

    return stats


def calc_band_from_limit(stats, limits, only_median=False):
    """

    """
    new_band = None

    for band, limit in reversed(limits.items()):
        bool_list = []
        if only_median:
            if 'median' in limit:
                min1, max1 = limit['median']
                bool0 = (stats['median'] > min1) & (stats['median'] <= max1)
                bool_list.append(bool0)
            else:
                raise ValueError('median not in limits.')
        else:
            for stat_name, minmax in limit.items():
                min1, max1 = minmax
                bool0 = (stats[stat_name] > min1) & (stats[stat_name] <= max1)
                bool_list.append(bool0)

        if all(bool_list):
            new_band = band

    return new_band


def get_limits(feature_parameter, tags):
    """

    """
    # nps_mod = importlib.import_module(version)
    nps_mod = v202401 # One day make this flexible...

    ## Get the limits
    limits = nps_mod.parameter_limits_dict[feature_parameter]

    ## Assign appropriate limits if it's a complicated limit...
    if feature_parameter in nps_mod.parameter_special_cols_dict:
        if tags is None:
            raise ValueError('tags must be assigned if there are special classes in the attribute.')
        tag_name = nps_mod.parameter_special_cols_dict[feature_parameter]
        tag = tags[tag_name]
        old_limits = copy(limits)
        limits = {}
        for band, lm in old_limits.items():
            limit = lm[tag]
            limits[band] = limit

    return limits


def calc_improvement_to_band(stats, limits, band, only_median=False):
    """

    """
    current_band = calc_band_from_limit(stats, limits, only_median)

    if band >= current_band:
        results = {stat: 0 for stat in stats}
    else:
        band_limits = limits[band]
        results = {}
        if only_median:
            stat = 'median'
            limit = band_limits[stat]
            current_val = stats[stat]
            if limit[0] == -1:
                ratio = round(1 - limit[1]/current_val, 4)
            else:
                ratio = round(limit[0]/current_val - 1, 4)

            results[stat] = ratio
        else:
            for stat, limit in band_limits.items():
                current_val = stats[stat]
                if limit[0] == -1:
                    ratio = round(1 - limit[1]/current_val, 4)
                else:
                    ratio = round(limit[0]/current_val - 1, 4)

                results[stat] = ratio

    return results


def url_to_file(url, file_path, chunk_size: int=524288, retries=3):
    """
    General function to get an object from an S3 bucket. One of s3, connection_config, or public_url must be used.

    Parameters
    ----------
    url: http str
        The http url to the file.
    chunk_size: int
        The amount of bytes to download as once.

    Returns
    -------
    file object
        file object of the S3 object.
    """
    transport_params = {'buffer_size': chunk_size, 'timeout': 120}

    ## Get the object
    counter = retries
    while True:
        try:
            file_obj = smart_open.open(url, 'rb', transport_params=transport_params, compression='disable')
            file_path1 = pathlib.Path(file_path)
            file_path1.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path1, 'wb') as f:
                chunk = file_obj.read(chunk_size)
                while chunk:
                    f.write(chunk)
                    chunk = file_obj.read(chunk_size)
            break
        except Exception as err:
            counter = counter - 1
            if counter > 0:
                sleep(3)
            else:
                print('smart_open could not open url with the following error:')
                print(err)
                file_obj = None
                break

    return file_obj


def check_files(data_path):
    """

    """
    data_path1 = pathlib.Path(data_path)

    files = [f.name for f in data_path1.glob('*') if f.name in file_dict]
    missing_files = []
    for f in file_dict:
        if f not in files:
            missing_files.append(file_dict[f])

    return missing_files


def download_files(data_path, only_missing=True):
    """

    """
    if only_missing:
        urls = check_files(data_path)
    else:
        urls = list(file_dict.values())

    print('Downloading: {}'.format(', '.join([os.path.split(url)[-1] for url in urls])))
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for url in urls:
            file_name = os.path.split(url)[-1]
            new_path = os.path.join(data_path, file_name)
            f = executor.submit(url_to_file, url, new_path)
            futures.append(f)
        _ = concurrent.futures.wait(futures)




