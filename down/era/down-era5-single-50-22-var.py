import cdsapi
import os

def down(yyyy,vvvv,mmmm):
    c = cdsapi.Client()

    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'format': 'netcdf',
            'variable': vvvv,
            'year': yyyy,
            'grid': [1.0, 1.0],
            'month': mmmm,
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
                '00:00', '03:00', '06:00',
                '09:00', '12:00', '15:00',
                '18:00', '21:00',
            ],
        },
        "era5_single_"+vvvv+"_"+str(yyyy)+mmmm+'_.nc')

year = [1959,2022]
vars_name  =  ['10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature',
                '2m_temperature', 'convective_available_potential_energy', 'convective_inhibition',
                'convective_precipitation', 'evaporation', 'large_scale_precipitation',
                'mean_sea_level_pressure', 'sea_surface_temperature', 'skin_temperature',
                'surface_latent_heat_flux', 'surface_net_solar_radiation', 'surface_net_thermal_radiation',
                'surface_pressure', 'surface_sensible_heat_flux', 'toa_incident_solar_radiation',
                'total_precipitation', 'vertical_integral_of_divergence_of_moisture_flux', 'vertical_integral_of_eastward_water_vapour_flux',
                'vertical_integral_of_northward_water_vapour_flux', 'vertically_integrated_moisture_divergence',]

month  =  [
                '01', '02', '03',
                '04', '05', '06',
                '07', '08', '09',
                '10', '11', '12',
            ]

files = os.listdir("/home/sun/segate/era5-single-hourly/")
#files.sort()
#files.pop()

for yyyy in range(year[0],year[1]+1):
    for vvvv in vars_name:
        for mmmm in month:
    
            down(yyyy,vvvv,mmmm)