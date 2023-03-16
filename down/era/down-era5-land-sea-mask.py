import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': 'land_sea_mask',
        'year': '1971',
        'grid':[1.0, 1.0],
        'month': '07',
        'day': '19',
        'time': '06:00',
    },
    'ERA5_land_sea_mask_1x1.nc')