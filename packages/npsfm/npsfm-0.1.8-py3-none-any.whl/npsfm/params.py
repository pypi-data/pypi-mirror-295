#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 10:28:31 2024

@author: mike
"""
import os
import pathlib

###################################################
### REC parameters

script_path = pathlib.Path(os.path.realpath(os.path.dirname(__file__)))
data_path = script_path.parent.joinpath('data')

if not data_path.is_dir():
    raise ValueError(f'{data_path} does not exist')

















































































