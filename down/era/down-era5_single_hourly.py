import cdsapi

c = cdsapi.Client()

def down(yyyy, vvvv):
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'grid': [1.0, 1.0],
            'variable': vvvv,
            'year': str(yyyy),
            'month': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ],
            'day': [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
                '13', '14', '15',
                '16', '17', '18',
                '19', '20', '21',
                '22', '23', '24',
                '25', '26', '27',
                '28', '29', '30',
                '31',
            ],
            'time': [
                '00:00', '01:00', '02:00',
                '03:00', '04:00', '05:00',
                '06:00', '07:00', '08:00',
                '09:00', '10:00', '11:00',
                '12:00', '13:00', '14:00',
                '15:00', '16:00', '17:00',
                '18:00', '19:00', '20:00',
                '21:00', '22:00', '23:00',
            ],
        },
        '/home/sun/segate2/era5-single-hourly/era5_hourly_single_'+vvvv+'_'+str(yyyy)+'.nc')

#varname = [
#                'mean_sea_level_pressure', '10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
#                '2m_temperature', 'evaporation',
#                'sea_surface_temperature', 'surface_latent_heat_flux', 'surface_net_solar_radiation',
#                'surface_net_thermal_radiation', 'surface_pressure', 'surface_sensible_heat_flux',
#                'total_precipitation',
#            ]
#varname = [
#                'mean_sea_level_pressure', 
#            ]
varname = [
                'surface_net_thermal_radiation', 'surface_pressure', 'surface_sensible_heat_flux',
                'total_precipitation',
            ]

for vvvv in varname:
    for yyyy in range(1940, 2023):
        down(yyyy, vvvv)
