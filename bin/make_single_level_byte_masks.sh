#!/bin/bash
# make_single_level_byte_masks.sh
#
# For PrimOday [uv]o, which should be on olevel, but only contain the surface
# level as 1 3d variable, copy the existing byte masks and just keep the
# surface level

byte_mask_dir="/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/bytes_masks"
declare -a resolutions=("HadGEM3-GC31-LL" "HadGEM3-GC31-MM")

byte_mask_file="primavera_byte_masks.nc"
output_file="primavera_single_level_byte_masks.nc"

for resolution in "${resolutions[@]}";
do
    res_dir=$byte_mask_dir/$resolution
    ncks -dlev,0 "$res_dir/$byte_mask_file" "$res_dir/$output_file";
done
