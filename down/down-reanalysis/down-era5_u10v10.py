'''
2021/10/11
本代码下载era5的10m风数据
'''
import cdsapi

c = cdsapi.Client()

def down_u10v10(yyyy,var):
    c.retrieve(
        'reanalysis-era5-single-levels',
        {
            'product_type': 'reanalysis',
            'variable': [
                var,
            ],
            'year': yyyy,
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
                '00:00',
                '03:00',
                '06:00',
                '09:00',
                '12:00',
                '15:00',
                '18:00',
                '21:00',
            ],
            'format': 'netcdf',
            'grid': [1.0, 1.0],
        },
        "/home/sun/mydown/era5_u10v10/"+str(yyyy)+"_"+var+'.nc')

vars   =   ['10m_u_component_of_wind']
for yyyy in range(1979,2022):
    for vvvv in vars:
        down_u10v10(yyyy,vvvv)

