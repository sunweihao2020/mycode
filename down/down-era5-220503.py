# 下载四月的看看今年会不会偏早
import cdsapi

c = cdsapi.Client()

c.retrieve(
    'reanalysis-era5-single-levels',
    {
        'product_type': 'reanalysis',
        'format': 'netcdf',
        'variable': [
            '10m_u_component_of_wind', '10m_v_component_of_wind', 'total_precipitation',
        ],
        'year': '2022',
        'month': '04',
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
            '28',
        ],
        'time': [
            '00:00', '06:00', '12:00',
            '18:00',
        ],
    },
    'download_era5_220503.nc')