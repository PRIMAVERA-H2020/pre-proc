#!/bin/bash
# make_known_good_grids.sh
#
# Copy known good ORCA grids for use in fixing the HadGEM PRIMAVERA grids.
# netCDF3 is required because the netCDF4 library sometimes struggles to
# rename dimensions.

output_dir="/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/grids"

nc_vars="latitude,longitude,vertices_latitude,vertices_longitude"

#########
# ORCA1 #
#########
grid="ORCA1"
mkdir -p "$output_dir/$grid"

# v-grid
sub_grid="v"
good_file="/badc/cmip6/data/CMIP6/CMIP/MOHC/HadGEM3-GC31-LL/historical/r1i1p1f3/Omon/vo/gn/v20190624/vo_Omon_HadGEM3-GC31-LL_historical_r1i1p1f3_gn_185001-189912.nc"
ncks -3 --no_alphabetize -v "$nc_vars" "$good_file" "${output_dir}/${grid}_grid-${sub_grid}.nc"