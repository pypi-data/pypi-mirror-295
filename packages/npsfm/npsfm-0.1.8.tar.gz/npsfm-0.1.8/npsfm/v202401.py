#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 17 16:36:04 2023

@author: mike
"""

#######################################################
### Parameters

## Base nps-fm from the 2023-02-23 version

# Rivers
river_chla_limits = {
                'A': {1: {'Q92': (-1, 50)},
                      2: {'Q83': (-1, 50)}},
                'B': {1: {'Q92': (-1, 120)},
                      2: {'Q83': (-1, 120)}},
                'C': {1: {'Q92': (-1, 200)},
                      2: {'Q83': (-1, 200)}},
                'D': {1: {'Q92': (-1, 100000)},
                      2: {'Q83': (-1, 100000)}}
                }

river_ammonia_limits = {
    'A': {'median': (-1, 0.03),
          'Q95': (-1, 0.05)},
    'B': {'median': (-1, 0.24),
          'Q95': (-1, 0.40)},
    'C': {'median': (-1, 1.3),
          'Q95': (-1, 2.2)},
    'D': {'median': (-1, 100000),
          'Q95': (-1, 100000)}
    }

river_nitrate_limits = {
                  'A': {'median': (-1, 1),
                        'Q95': (-1, 1.5)},
                  'B': {'median': (-1, 2.4),
                        'Q95': (-1, 3.5)},
                  'C': {'median': (-1, 6.9),
                        'Q95': (-1, 9.8)},
                  'D': {'median': (-1, 100000),
                        'Q95': (-1, 100000)}
                  }

river_ecoli_limits = {
                  'A': {'G540': (-1, 0.05),
                        'G260': (-1, 0.2),
                        'median': (-1, 130),
                        'Q95': (-1, 540)},
                  'B': {'G540': (-1, 0.1),
                        'G260': (-1, 0.3),
                        'median': (-1, 130),
                        'Q95': (-1, 1000)},
                  'C': {'G540': (-1, 0.2),
                        'G260': (-1, 0.34),
                        'median': (-1, 130),
                        'Q95': (-1, 1200)},
                  'D': {'G540': (-1, 0.3),
                        'G260': (-1, 1.01),
                        'median': (-1, 1000000),
                        'Q95': (-1, 1000000)},
                  'E': {'G540': (-1, 1.01),
                        'G260': (-1, 1.01),
                        'median': (-1, 1000000),
                        'Q95': (-1, 1000000)}
                  }

river_mci_limits = {
                'A': {'mean': (130, 100000)},
                'B': {'mean': (110, 100000)},
                'C': {'mean': (90, 100000)},
                'D': {'mean': (-1, 100000)}
                }

river_drp_limits = {
                'A': {'median': (-1, 0.006),
                      'Q95': (-1, 0.021)},
                'B': {'median': (-1, 0.01),
                      'Q95': (-1, 0.03)},
                'C': {'median': (-1, 0.018),
                      'Q95': (-1, 0.054)},
                'D': {'median': (-1, 100000),
                      'Q95': (-1, 100000)}
                }

river_clarity_limits = {
                'A': {1: {'median': (1.78, 100000)},
                      2: {'median': (0.93, 100000)},
                      3: {'median': (2.95, 100000)},
                      4: {'median': (1.38, 100000)}},
                'B': {1: {'median': (1.55, 100000)},
                      2: {'median': (0.76, 100000)},
                      3: {'median': (2.57, 100000)},
                      4: {'median': (1.17, 100000)}},
                'C': {1: {'median': (1.34, 100000)},
                      2: {'median': (0.61, 100000)},
                      3: {'median': (2.22, 100000)},
                      4: {'median': (0.98, 100000)}},
                'D': {1: {'median': (-1, 100000)},
                      2: {'median': (-1, 100000)},
                      3: {'median': (-1, 100000)},
                      4: {'median': (-1, 100000)}}
                }

river_dep_sed_limits = {
                'A': {1: {'median': (-1, 7)}, 2: {'median': (-1, 10)},
                      3: {'median': (-1, 9)}, 4: {'median': (-1, 13)}},
                'B': {1: {'median': (-1, 14)}, 2: {'median': (-1, 19)},
                      3: {'median': (-1, 18)}, 4: {'median': (-1, 19)}},
                'C': {1: {'median': (-1, 21)}, 2: {'median': (-1, 29)},
                      3: {'median': (-1, 27)}, 4: {'median': (-1, 27)}},
                'D': {1: {'median': (-1, 100000)}, 2: {'median': (-1, 100000)},
                      3: {'median': (-1, 100000)}, 4: {'median': (-1, 100000)}}
                }

river_fish_limits = {
                'A': {'mean': (34, 100000)},
                'B': {'mean': (28, 100000)},
                'C': {'mean': (18, 100000)},
                'D': {'mean': (-1, 100000)}
                }

# Lakes
lake_ecoli_limits = {
    'A': {
        'G540': (-1, 0.05),
        'G260': (-1, 0.2),
        'median': (-1, 130),
        'Q95': (-1, 540)
        },
    'B': {
        'G540': (-1, 0.1),
        'G260': (-1, 0.3),
        'median': (-1, 130),
        'Q95': (-1, 1000)
        },
    'C': {
        'G540': (-1, 0.2),
        'G260': (-1, 0.34),
        'median': (-1, 130),
        'Q95': (-1, 1200)
        },
    'D': {
        'G540': (-1, 0.3),
        'G260': (-1, 1.01),
        'median': (-1, 1000000),
        'Q95': (-1, 1000000)
        },
    'E': {
        'G540': (-1, 1.01),
        'G260': (-1, 1.01),
        'median': (-1, 1000000),
        'Q95': (-1, 1000000)
        }
    }

lake_ammonia_limits = {
    'A': {'median': (-1, 0.03),
          'Q95': (-1, 0.05)},
    'B': {'median': (-1, 0.24),
          'Q95': (-1, 0.40)},
    'C': {'median': (-1, 1.3),
          'Q95': (-1, 2.2)},
    'D': {'median': (-1, 100000),
          'Q95': (-1, 100000)}
    }

lake_tp_limits = {
    'A': {'median': (-1, 10)},
    'B': {'median': (-1, 20)},
    'C': {'median': (-1, 50)},
    'D': {'median': (-1, 100000)}
    }

lake_chla_limits = {
    'A': {'median': (-1, 2),
          'max': (-1, 10)},
    'B': {'median': (-1, 5),
          'max': (-1, 25)},
    'C': {'median': (-1, 12),
          'max': (-1, 60)},
    'D': {'median': (-1, 100000),
          'max': (-1, 100000)}
    }

lake_tn_limits = {
    'A': {
        'stratified': {'median': (-1, 160)},
        'polymictic': {'median': (-1, 300)},
        },
    'B': {
        'stratified': {'median': (-1, 350)},
        'polymictic': {'median': (-1, 500)},
        },
    'C': {
        'stratified': {'median': (-1, 750)},
        'polymictic': {'median': (-1, 800)},
        },
    'D': {
        'stratified': {'median': (-1, 100000)},
        'polymictic': {'median': (-1, 100000)},
        }
    }

lake_cyano_limits = {
    'A': {'Q80': (-1, 0.5),
          },
    'B': {'Q80': (-1, 1),
          },
    'C': {'Q80': (-1, 10),
          },
    'D': {'Q80': (-1, 100000),
          }
    }


# Combo
# bottom_line_limits = {
#     ('river', 'Ammonia'): {'median': (-1, 0.24),
#                            'Q95': (-1, 0.40)},
#     ('river', 'Nitrate'): {'median': (-1, 2.4),
#                            'Q95': (-1, 3.5)},
#     ('river', 'MCI'): {'mean': (90, 100000)},
#     ('river', 'Clarity'): {1: {'median': (1.34, 100000)},
#                            2: {'median': (0.61, 100000)},
#                            3: {'median': (2.22, 100000)},
#                            4: {'median': (0.98, 100000)}
#                            },
#     ('river', 'Dep Sediment'): {1: {'median': (-1, 21)},
#                                 2: {'median': (-1, 29)},
#                                 3: {'median': (-1, 27)},
#                                 4: {'median': (-1, 27)}
#                                 },
#     ('river', 'Chla'): {1: {'Q92': (-1, 200)},
#                         2: {'Q83': (-1, 200)}
#                         },
#     ('lake', 'Ammonia'): {'median': (-1, 0.24),
#                           'Q95': (-1, 0.40)},
#     ('lake', 'Cyano'): {
#         'Q80': (-1, 10),
#         },
#     ('lake', 'Chla'): {
#         'median': (-1, 12),
#         'max': (-1, 60)
#         },
#     ('lake', 'Total nitrogen'): {
#         True: (-1, 750),
#         False: (-1, 800),
#         },
#     ('lake', 'Total phosphorus'): {'median': (-1, 50)},
#     }


bottom_line_limits = {
    ('river', 'Ammonia'): 'B',
    ('river', 'Nitrate'): 'B',
    ('river', 'MCI'): 'C',
    ('river', 'Clarity'): 'C',
    ('river', 'Dep Sediment'): 'C',
    ('river', 'Chla'): 'C',
    ('river', 'DRP'): 'D',
    ('river', 'E.coli'): 'E',
    ('lake', 'Ammonia'): 'B',
    ('lake', 'Cyano'): 'C',
    ('lake', 'Chla'):'C',
    ('lake', 'Total nitrogen'): 'C',
    ('lake', 'Total phosphorus'): 'C',
    }


parameter_special_cols_dict = {
    ('river', 'Clarity'): 'ss_class',
    ('river', 'Dep Sediment'): 'ds_class',
    ('river', 'Chla'): 'peri_class',
    ('lake', 'Total nitrogen'): 'stratified',
    }

parameter_limits_dict = {
    ('river', 'Chla'): river_chla_limits,
    ('river', 'Ammonia'): river_ammonia_limits,
    ('river', 'Nitrate'): river_nitrate_limits,
    ('river', 'Clarity'): river_clarity_limits,
    ('river', 'E.coli'): river_ecoli_limits,
    ('river', 'MCI'): river_mci_limits,
    ('river', 'DRP'): river_drp_limits,
    ('river', 'Dep Sediment'): river_dep_sed_limits,
    ('river', 'Fish IBI'): river_fish_limits,
    ('lake', 'Ammonia'): lake_ammonia_limits,
    ('lake', 'Cyano'): lake_cyano_limits,
    ('lake', 'Chla'): lake_chla_limits,
    ('lake', 'Total nitrogen'): lake_tn_limits,
    ('lake', 'Total phosphorus'): lake_tp_limits,
    ('lake', 'E.coli'): lake_ecoli_limits,
    }


######################################################
### Models















































































