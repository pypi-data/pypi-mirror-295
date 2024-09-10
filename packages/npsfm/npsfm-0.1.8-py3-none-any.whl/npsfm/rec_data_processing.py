#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 14:40:44 2023

@author: mike
"""
import io
import os
import pathlib
import pandas as pd
import geopandas as gpd
import nzrec
import booklet

import params

pd.options.display.max_columns = 10


#######################################################
### Parameters

# data_path = pathlib.Path(os.path.join(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0], 'data'))

way_id = 3133749

nzrec_data_path = '/home/mike/git/nzrec/data'

## Extra data
sed_csv = 'sediment-classes-for-rec24-nzsegments.csv.zip'

## Output
# agg_conc_csv = 'wairarapa_stream_data.csv'
# agg_conc_feather = 'river_data.feather'

rec_classes_blt_path = params.data_path.joinpath('rec_tags.blt')



#####################################################
### Processing

rec_tags = {}

w0 = nzrec.Water(nzrec_data_path)


# tags = w0._way_tag[way_id]

for way_id, tags in w0._way_tag.items():

    ## Periphyton classes
    climate = tags['Climate class']
    geology = tags['Geology class']

    if (climate in ('WD', 'CD')) and (geology in ('SS', 'VA', 'VB')):
        peri_class = 2
    else:
        peri_class = 1

    rec_tags[way_id] = {'peri_class': peri_class}

    ## SS class
    ss_class = tags['Suspended_4_class']
    if (ss_class is None):
        ss_class = 1
    rec_tags[way_id].update({'ss_class': ss_class})

    ## deposited sediment class
    ds_class = tags['Deposited_4_class']
    if (ds_class is None) or (ds_class == 'naturally soft-bottomed'):
        ds_class = 0
    rec_tags[way_id].update({'ds_class': ds_class})

### Save results
# data_path.mkdir(parents=True, exist_ok=True)

with booklet.open(rec_classes_blt_path, 'n', key_serializer='uint4', value_serializer='msgpack', n_buckets=6000011) as f:
    f.update(rec_tags)

w0.close()

































