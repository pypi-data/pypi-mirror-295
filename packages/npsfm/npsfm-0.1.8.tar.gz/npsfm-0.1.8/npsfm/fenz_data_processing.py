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
# import nzrec
import booklet

import params

pd.options.display.max_columns = 10


#######################################################
### Parameters

# data_path = pathlib.Path(os.path.join(os.path.split(os.path.realpath(os.path.dirname(__file__)))[0], 'data'))

way_id = 3133749

nzrec_data_path = '/home/mike/git/nzrec/data'

## Extra data
lake_poly_gpkg_path = params.data_path.joinpath('lake_polygons_fenz.gpkg')

## Output
# agg_conc_csv = 'wairarapa_stream_data.csv'
# agg_conc_feather = 'river_data.feather'

lake_tags_blt_path = params.data_path.joinpath('lake_tags.blt')



#####################################################
### Processing

lakes_poly0 = gpd.read_file(lake_poly_gpkg_path)
lakes_poly0 = lakes_poly0[lakes_poly0.LFENZID > 0].copy()
lakes_poly0['LFENZID'] = lakes_poly0['LFENZID'].astype('int32')
lakes_poly1 = lakes_poly0.drop('geometry', axis=1).drop_duplicates('LFENZID').set_index('LFENZID')

lake_tags = {}
for lake_id, tags in lakes_poly1.iterrows():
    if tags['MaxDepth'] <= 7.5:
        stratified = 'polymictic'
    else:
        stratified = 'stratified'

    tags_dict = tags.to_dict()
    tags_dict['stratified'] = stratified

    lake_tags[lake_id] = tags_dict

### Save results
with booklet.open(lake_tags_blt_path, 'n', key_serializer='uint4', value_serializer='msgpack', n_buckets=10007) as f:
    f.update(lake_tags)


































