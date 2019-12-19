#!/bin/bash
# make_height2m_reference.sh
# Make a referenec file that just contains a height variable with a value of 2 m.

INPUT_FILE=/badc/cmip6/data/CMIP6/HighResMIP/CNRM-CERFACS/CNRM-CM6-1/highresSST-present/r1i1p1f2/\
Amon/tas/gr/v20190214/tas_Amon_CNRM-CM6-1_highresSST-present_r1i1p1f2_gr_195001-195912.nc
OUTPUT_DIR=/gws/nopw/j04/primavera1/cache/jseddon/reference_files
OUTPUT_FILE=height2m_reference.nc
OUTPUT_PATH="$OUTPUT_DIR/$OUTPUT_FILE"

mkdir -p "$OUTPUT_DIR"

ncks -v height "$INPUT_FILE" "$OUTPUT_PATH"

# check that the height value is definitely 2m
h2m_val=$(ncdump -v height "$OUTPUT_PATH" | grep 'height =')
if [ "$h2m_val" != " height = 2 ;" ]; then 
    echo "Height is not 2 m in $OUTPUT_PATH";
    exit 1;
fi

