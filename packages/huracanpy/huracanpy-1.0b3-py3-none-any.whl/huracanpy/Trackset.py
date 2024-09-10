#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:22:47 2024

@author: bourdin
"""

import xarray as xr
import pandas as pd

from ._data import save
from . import utils
from . import diags
from . import plot
from . import assess
from . import subset

class Trackset(xr.Dataset):
    pass
    
def nunique(self):
    return pd.Series(self).nunique()
xr.DataArray.nunique = nunique

# Save
Trackset.save = save

# Add utils as methods
## Geography
# Trackset.add_all_info = utils.add_all_info # TODO: Understand why it does not work
Trackset.get_hemisphere = utils.geography.get_hemisphere
Trackset.get_basin = utils.geography.get_basin
Trackset.get_land_or_ocean = utils.geography.get_land_or_ocean
Trackset.get_country = utils.geography.get_country
Trackset.get_continent = utils.geography.get_continent
## Category
# Trackset.categorize = utils.category.categorize # -> To be a method of arrays themselves
Trackset.get_sshs_cat = utils.category.get_sshs_cat
Trackset.get_pressure_cat = utils.category.get_pressure_cat
## Time
# get_time
Trackset.expand_time = utils.time.expand_time
Trackset.get_season = utils.time.get_season
## Interp
Trackset.interp_time = utils.interp.interp_time
## ACE
# ace_by_point -> To be for arrays themselves

# TODO add "add" functions

# Add diags as methods
## Track density
Trackset.track_density = diags.track_density.simple_global_histogram
## Track stats
Trackset.ace_by_track = diags.track_stats.ace_by_track
Trackset.duration = diags.track_stats.duration 
Trackset.gen_vals = diags.track_stats.gen_vals 
Trackset.extremum_vals = diags.track_stats.extremum_vals 
## Translation speed
Trackset.translation_speed = diags.translation_speed 
## Lifecycle
Trackset.time_from_genesis = diags.lifecycle.time_from_genesis 
Trackset.time_from_extremum = diags.lifecycle.time_from_extremum 
## Rate
Trackset.rate = diags.rate 
## Climato
Trackset.freq = diags.climato.freq 
Trackset.TC_days = diags.climato.TC_days
Trackset.ACE = diags.climato.ACE 

# Plot
## Plot tracks
Trackset.plot_tracks = plot.plot_tracks_basic

# Assess
## Match
Trackset.match_with = assess.match_pair

# Subset
Trackset.sel_id = subset.sel_id