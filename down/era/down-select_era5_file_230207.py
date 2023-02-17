import cdsapi

def down(yyyy,mmmm,vvvv,dddd):
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-pressure-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': vvvv,
            'pressure_level': [
                '10', '30',
                '50', '100',
                '150',
                '200', '250',
                '300', '350', '400',
                '450', '500', '550',
                '600', '650', '700',
                '750', '775', '800',
                '825', '850', '875',
                '900', '925', '950',
                '975', '1000',
            ],
            'grid': [1.0, 1.0],
            'year': str(yyyy),
            'month': mmmm,
            'day':dddd,
            'time': [
                '00:00',
                '03:00',
                '06:00',
                '09:00',
                '12:00',
                '15:00',
                '18:00',
                '21:00',
            ],
        },
        vvvv+'_'+str(yyyy)+mmmm+dddd+'.nc')

#down(1979, '01', 'u_component_of_wind', '01')
#down(1979, '01', 'u_component_of_wind', '02')
#down(1979, '01', 'u_component_of_wind', '03')
down(1979, '01', 'u_component_of_wind', '05')