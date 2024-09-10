#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 15:00:43 2023

@author: mike
"""
import os
import pathlib
import pandas as pd
import numpy as np
from copy import copy
import booklet

from . import v202401, utils
# import v202401, utils


pd.options.display.max_columns = 10

######################################################
### Parameters

# features = set([limits[0] for limits in v202401.parameter_limits_dict])
# indicators = set([limits[1] for limits in v202401.parameter_limits_dict])



#######################################################
### Functions







###################################################
### Classes


# class ImportData:
#     """

#     """
#     def __init__(self, ts_data=None, indicator=None, nzsegment=None):
#         """

#         """



#     def add_data(self, ts_data, indicator, feature):
#         """

#         """
#         ## Checks
#         if not isinstance(ts_data, pd.Series):
#             raise TypeError('ts_data must be a pandas Series with a datetime index.')
#         if not isinstance(ts_data.index, pd.DatetimeIndex):
#             raise TypeError('ts_data must be a pandas Series with a datetime index.')
#         if indicator not in indicators:
#             raise ValueError(f'indicator must be one of {indicators}')
#         if feature not in features:
#             raise ValueError(f'feature must be one of {features}')




#     def add_nzsegment(self, nzsegment):
#         """

#         """





class NPSFM:
    """

    """
    def __init__(self, package_data_path, download_files=False, only_missing=True):
        """

        """
        ## File check
        missing_files = utils.check_files(package_data_path)
        if missing_files:
            if download_files:
                utils.download_files(package_data_path, only_missing=only_missing)
            else:
                raise ValueError('There are missing data files. Files would have been downloaded if download_files=True (but it is not). Othersize if this was a mistake, please check/change the data_path: {}'.format(', '.join([os.path.split(f)[-1] for f in missing_files])))

        self.data_path = pathlib.Path(package_data_path)

        ## Run checks to see what parameters are available to calc grades


    def add_limits(self, feature, parameter, nzsegment=None, lfenzid=None):
        """

        """
        ## Checks
        feature_parameter = (feature, parameter)
        if feature_parameter not in v202401.parameter_limits_dict:
            raise ValueError(f'The combo of {feature_parameter} must be one of {list(v202401.parameter_limits_dict.keys())}')
        if isinstance(nzsegment, int):
            file_path = self.data_path.joinpath('rec_tags.blt')
            tag_id = nzsegment
        elif isinstance(lfenzid, int):
            file_path = self.data_path.joinpath('lake_tags.blt')
            tag_id = lfenzid
        else:
            tag_id = None
            tags = None
        if tag_id:
            with booklet.open(file_path) as f:
                if tag_id not in f:
                    raise ValueError(f'{tag_id} not a valid id.')
                else:
                    tags = f[tag_id]

        ## Remove old ts_data and stats if they exists
        if hasattr(self, 'ts_data'):
            delattr(self, 'ts_data')
            delattr(self, 'stats')

        ## Determine the associated limits for the site and parameter
        limits = utils.get_limits(feature_parameter, tags)

        bl_limit_band = v202401.bottom_line_limits[feature_parameter]
        bl_limit = limits[bl_limit_band]

        ## Save data
        self.parameter = parameter
        self.feature = feature
        self.feature_parameter = feature_parameter
        # self.nzsegment = nzsegment
        self.class_tags = tags
        self.bottom_line_limit_band = bl_limit_band
        self.bottom_line_limit = bl_limit
        self.limits = limits

        return limits


    def add_stats(self, ts_data):
        """

        """
        ## Checks
        if not hasattr(self, 'limits'):
            raise ValueError('You must run the add_limits method first.')
        if not isinstance(ts_data, pd.Series):
            raise TypeError('ts_data must be a pandas Series with a datetime index.')
        if not isinstance(ts_data.index, pd.DatetimeIndex):
            raise TypeError('ts_data must be a pandas Series with a datetime index.')

        ## Determine the stats
        self.stats = utils.calc_stats(ts_data, self.limits)

        return self.stats


    def calc_band(self, only_median=False):
        """

        """
        result = utils.calc_band_from_limit(self.stats, self.limits, only_median)

        return result


    def calc_improvement_to_band(self, band, only_median=False):
        """

        """
        if band not in self.limits:
            raise ValueError(f'{band} not in the available bands: {list(self.limits.keys())}')

        results = utils.calc_improvement_to_band(self.stats, self.limits, band, only_median)

        return results


    def calc_improvement_to_bottom_line(self, only_median=False):
        """

        """
        results = utils.calc_improvement_to_band(self.stats, self.limits, self.bottom_line_limit_band, only_median)

        return results




####################################################
### Testing























































