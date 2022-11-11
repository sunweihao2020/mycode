'''
This code calculate daymean for era5 hourly data
'''

var_names =  ['temp','uwind','vwind']
path0     =  '/data1/ERA5/datasets/muti-levels/hourly/'

def cdo_daymean(var_name,year,path_out):
    import os

    path1  =  path0  +  var_name  +  '/'

    file_list  =  os.listdir(path1)
    files      =  []

    for ffff in file_list:
        if (var_name in ffff) and (".nc" in ffff) and (str(year) in ffff):
            files.append(ffff)

    for ff in files:
        os.system("cdo daymean "+ path0 + var_name + '/' + ff +" "+ path_out +ff)

def main():
    "下为例子，在参数中输入变量，年份，输出数据的路径即可"
    cdo_daymean('temp',2020,'/data5/2019swh/test_data/')

if __name__ == '__main__':
    main()