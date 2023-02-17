'''
2023-1-17
因为我下载era5数据有些数据有问题,这里我是把没下载成功的输出到一个列表里面,下载指定的文件
'''
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
            'year': yyyy,
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
        vvvv+'_'+yyyy+mmmm+dddd+'.nc')

# 1. First: read the diff files
diff_file = open("/home/sun/data/other_data/diff_file.txt", "r")
diff      = diff_file.read()

data_into_list = diff.split("\n")
#print(data_into_list[5][:-12])

for element in data_into_list:
    date_message  =  element[-11:-3]
    var_name      =  element[:-12]

    down(yyyy=date_message[:4], mmmm=date_message[4:6], dddd=date_message[6:8], vvvv=var_name)