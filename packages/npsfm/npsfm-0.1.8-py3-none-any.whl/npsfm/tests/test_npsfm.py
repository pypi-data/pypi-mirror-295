#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 18 13:53:36 2024

@author: mike
"""
import pandas as pd
import os
import pathlib
import pytest

from npsfm import NPSFM

########################################################3
### Parameters

script_path = pathlib.Path(os.path.realpath(os.path.dirname(__file__)))
data_path = script_path.parent.parent.joinpath('data')

nzsegment = 3076139
parameter = 'Nitrate'
feature = 'river'
version = 'v202401'
hopeful_band = 'A'

########################################################
### Test

ts_data = pd.read_csv(script_path.joinpath('test_data1.csv.zip'), index_col=0, parse_dates=True)['value']


self = NPSFM(data_path, download_files=True)


def test_add_limits():
    limits = self.add_limits(feature, parameter, nzsegment)

    assert len(limits) == 4


limits = self.add_limits(feature, parameter, nzsegment)


def test_add_stats():
    stats = self.add_stats(ts_data)

    assert len(stats) == 2


stats = self.add_stats(ts_data)


def test_calc_band():
    attr_band = self.calc_band(only_median=True)
    attr_band = self.calc_band(only_median=False)

    assert attr_band == 'C'


def test_calc_improvement_to_band():
    improve_ratio1 = self.calc_improvement_to_band(hopeful_band, only_median=True)
    improve_ratio2 = self.calc_improvement_to_bottom_line(only_median=True)

    improve_ratio1 = self.calc_improvement_to_band(hopeful_band)
    improve_ratio2 = self.calc_improvement_to_bottom_line()

    assert (len(improve_ratio1) == 2) and len(improve_ratio2) == 2































































