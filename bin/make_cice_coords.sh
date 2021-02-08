#!/bin/bash
# make_cice_coords.sh
#
# Convert the CICE replacement coordinate files to netCDF3 and reame the dimensions so
# that they match the data files. netCDF3 is required because the netCDF4
# library sometimes struggles to rename dimensions.

cice_coord_dir="/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/cice_coords"
declare -a resolutions=("eORCA1" "eORCA025" "eORCA12")

for resolution in "${resolutions[@]}";
do
    res_dir=$cice_coord_dir/$resolution
    input_file="cice_${resolution}_coords.nc"
    t_file="cice_${resolution}_coords_grid-t.nc"
    uv_file="cice_${resolution}_coords_grid-uv.nc"

    ncks -h --no_alphabetize -3 "$res_dir/$input_file" "$res_dir/$t_file"
    ncrename -h -d nj,j -d ni,i -d nvertices,vertices -v TLAT,latitude -v TLON,longitude -v latt_bounds,vertices_latitude -v lont_bounds,vertices_longitude "$res_dir/$t_file"
    ncatted -h -a bounds,latitude,m,c,'vertices_latitude' -a long_name,latitude,d,, -a nav_model,latitude,d,, -a bounds,longitude,m,c,'vertices_longitude' -a long_name,longitude,d,, -a nav_model,longitude,d,, -a history,global,d,, "$res_dir/$t_file"

    ncks -h --no_alphabetize -3 "$res_dir/$input_file" "$res_dir/$uv_file"
    ncrename -d nj,j -d ni,i -d nvertices,vertices -v ULAT,latitude -v ULON,longitude -v latu_bounds,vertices_latitude -v lonu_bounds,vertices_longitude "$res_dir/$uv_file"
    ncatted -h -a bounds,latitude,m,c,'vertices_latitude' -a long_name,latitude,d,, -a nav_model,latitude,d,, -a bounds,longitude,m,c,'vertices_longitude' -a long_name,longitude,d,, -a nav_model,longitude,d,, -a history,global,d,, "$res_dir/$uv_file"
done
