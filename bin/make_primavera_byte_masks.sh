#!/bin/bash
# make_primavera_byte_masks.sh
#
# Convert the ocean byte mask files to netCDF3 and rename the dimensions so
# that they match the data files

byte_mask_dir="/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/bytes_masks"
declare -a resolutions=("HadGEM3-GC31-LL" "HadGEM3-GC31-MM")

byte_mask_file="ocean_byte_masks.nc"
temp_file="temp_byte_masks.nc"
output_file="primavera_byte_masks.nc"

rename_code="-d x,i -d y,j -d deptht,lev"

for resolution in "${resolutions[@]}";
do
    res_dir=$byte_mask_dir/$resolution
    ncks -3 "$res_dir/$byte_mask_file" "$res_dir/$temp_file";
    ncrename "$rename_code" "$res_dir/$temp_file" "$res_dir/$output_file";
    rm "$res_dir/$temp_file";
done


