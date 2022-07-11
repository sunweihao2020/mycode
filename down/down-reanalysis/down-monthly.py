import cdsapi
import os
def down(mmmm,vvvv):
    c = cdsapi.Client()
    c.retrieve(
        'reanalysis-era5-land-monthly-means',
        {
            'product_type': 'monthly_averaged_reanalysis',
            'format': 'netcdf',
            'variable': vvvv,
            'year': str(yyyy),
            'month': mmmm,
            'time': '00:00',
        },
        vvvv+'_'+str(yyyy)+mmmm+'.nc')

year = yyyy

files = os.listdir("/data1/other_data/DataUpdate/ERA5/new-era5/monthly/single/"+str(year)+"/")
month=['01', '02', '03','04', '05', '06','07', '08', '09','10', '11', '12']
var=['10m_u_component_of_wind', '10m_v_component_of_wind', '2m_dewpoint_temperature','2m_temperature', 'skin_temperature', 'surface_latent_heat_flux','surface_net_solar_radiation', 'surface_pressure', 'surface_sensible_heat_flux','total_precipitation']
for mmmm in range(0,len(month)):
    for vvvv in range(0,len(var)):
        name = var[vvvv]+'_'+str(yyyy)+month[mmmm]+'.nc'
        if name in files:
            continue
        else:
            down(month[mmmm],var[vvvv])  


