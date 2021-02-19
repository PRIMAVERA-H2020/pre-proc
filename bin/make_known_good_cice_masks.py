#!/usr/bin/env python
"""
make_known_good_cice_masks.py

Copy known good CICE masks for use in fixing the HadGEM CICE masks.
"""
import os

import numpy as np
from netCDF4 import Dataset

OUTPUT_DIR = "/gws/nopw/j04/primavera1/masks/HadGEM3Ocean_fixes/cice_masks"


def main():
    """main entry"""
    rootgrp = Dataset(os.path.join(OUTPUT_DIR, "primavera_cice_orca1_uv.nc"),
                      "w", format="NETCDF3_CLASSIC")
    print(os.path.join(OUTPUT_DIR, "primavera_cice_orca1_uv.nc"))
    mask = np.zeros((330, 360))
    mask[-1, 180:] += 1
    _i = rootgrp.createDimension('i', 360)
    _j = rootgrp.createDimension('j', 330)
    mask_variable = rootgrp.createVariable('mask', 'i4', ('j', 'i'))
    mask_variable.units = '1'
    mask_variable[:] = mask
    rootgrp.close()

    print(os.path.join(OUTPUT_DIR, "primavera_cice_orca025_t.nc"))
    rootgrp = Dataset(os.path.join(OUTPUT_DIR, "primavera_cice_orca025_t.nc"),
                      "w", format="NETCDF3_CLASSIC")
    mask = np.zeros((1205, 1440))
    mask[-1, 720:] += 1
    _i = rootgrp.createDimension('i', 1440)
    _j = rootgrp.createDimension('j', 1205)

    mask_variable = rootgrp.createVariable('mask', 'i4', ('j', 'i'))
    mask_variable.units = '1'
    mask_variable[:] = mask
    rootgrp.close()

    print(os.path.join(OUTPUT_DIR, "primavera_cice_orca12_t.nc"))
    rootgrp = Dataset(os.path.join(OUTPUT_DIR, "primavera_cice_orca12_t.nc"),
                      "w", format="NETCDF3_CLASSIC")
    mask = np.zeros((3604, 4320))
    mask[-1, 2160:] += 1
    _i = rootgrp.createDimension('i', 4320)
    _j = rootgrp.createDimension('j', 3604)

    mask_variable = rootgrp.createVariable('mask', 'i4', ('j', 'i'))
    mask_variable.units = '1'
    mask_variable[:] = mask
    rootgrp.close()


if __name__ == "__main__":
    main()
