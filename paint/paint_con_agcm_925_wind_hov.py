'''
2022-11-20
This code paint the hov diagram for the AGCM experiment using SST derived from CGCM con
'''
import sys
import xarray as xr
import numpy as np
module_path = ["/home/sun/mycode/module/","/data5/2019swh/mycode/module/"]
sys.path.append(module_path[0])
from module_sun import *
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.gridspec as gridspec

sys.path.append("/home/sun/mycode/paint/")
from paint_lunwen_version3_0_fig2b_2m_tem_wind_20220426 import save_fig

'''设置colormap、levels、坐标值'''
# 坐标轴设置
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
viridis = cm.get_cmap('Blues', 20)
newcolors = viridis(np.linspace(0, 1, 20))
#newcolors[5]  =  [1, 1, 1, 1.]
newcmp = ListedColormap(newcolors)
newcmp.set_under('white')
newcmp.set_over('#19345e')
#levels
clevs = np.arange(-5,5,11)
# Tick labels
x_tick_labels = []
for xx in range(70,131,20):
    x_tick_labels.append(u''+str(xx)+"\N{DEGREE SIGN}E")
y_tick = [100,110,120,130,140,150,161,171,181,191,201]
y_label = ['10Apr','20Apr','30Apr','10May','20May','30May','10Jun','20Jun','30Jun','10Jul','20Jul']

def lon_avg_wind_925(time_slice=slice(99,200),lat_slice=slice(10,15),lon_slice=slice(65,130),level=850):
    '''deal with model output'''
    data_path0  =  '/home/sun/data/model_data/f2000_ensemble/'
    data_path1  =  '/home/sun/data/model_data/climate/'

    agcm_prect  =  xr.open_dataset(data_path0 + 'U_climate2.nc').sel(time=time_slice,lat = lat_slice,lon = lon_slice,lev=level)
    cgcm_prect  =  xr.open_dataset(data_path1 + 'b1850_control_climate_atmosphere.nc').sel(time=time_slice,lat = lat_slice,lon = lon_slice,lev=level)

    # calculate weight average
    avg_cgcm_prect  =  (cgcm_prect["U"]*(np.cos(np.deg2rad(cgcm_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(cgcm_prect.lat.values)))
    avg_agcm_prect  =  (agcm_prect["U"]*(np.cos(np.deg2rad(agcm_prect.lat.values)))[None, :, None]).sum(dim='lat')/np.sum(np.cos(np.deg2rad(agcm_prect.lat.values)))

    print(avg_agcm_prect)
    return avg_agcm_prect,avg_cgcm_prect

def paint_model_hov(model,path_out,filename,time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''This function paint two panels:
        1. hovmoller diagram for the control CGCM experiment
        2. hovmoller diagram for the control AGCM experiment
    '''
    data_path       =  '/home/sun/data/model_data/climate/'
    f0              =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(30,18))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=2)

    j = 0
    name   =  ["CON_AGCM","CON_CGCM"]

    clevs  =  np.linspace(-10,10,11)

    for col in range(2):
        ax = fig1.add_subplot(spec1[0,col])

        # 设置坐标轴
        ax.set_xticks(np.arange(70,131,20))
        ax.set_xticklabels(x_tick_labels,fontsize=30)
        ax.set_yticks(y_tick)
        ax.set_yticklabels(y_label,fontsize=30)

        ax.set_title(name[j],fontsize=45,loc='left')

        if j == 0:
            cf   = ax.contourf(f0.lon.values, f0.time.values,0.99 * model[j], clevs, cmap='coolwarm', extend='both')
            cs   = ax.contour(f0.lon.values,  f0.time.values,0.99 * model[j], clevs, colors='k', linewidths=1)
        else:
            cf   = ax.contourf(f0.lon.values, f0.time.values,1.05 * model[j], clevs, cmap='coolwarm', extend='both')
            cs   = ax.contour(f0.lon.values,  f0.time.values,1.05 * model[j], clevs, colors='k', linewidths=1)


        j += 1
    
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(cf, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.tick_params(labelsize=20)
    save_fig(path_out=path_out,file_out=filename)

def paint_model_hov_diff(model,path_out,filename,time_slice=slice(100,201),lat_slice=slice(10,20),lon_slice=slice(65,130)):
    '''This function paint two panels:
        1. hovmoller diagram for the control CGCM experiment
        2. hovmoller diagram for the control AGCM experiment
    '''
    viridis = cm.get_cmap('coolwarm')
    newcolors = viridis(np.linspace(0, 1, 30))
    newcolors[14]  =  [1, 1, 1, 1.]
    newcolors[15]  =  [1, 1, 1, 1.]
    newcolors[16]  =  [1, 1, 1, 1.]

    newcmp = ListedColormap(newcolors)
    newcmp.set_under('blue')
    newcmp.set_over('red')
    data_path       =  '/home/sun/data/model_data/climate/'
    f0              =  xr.open_dataset(data_path + "b1850_control_atmosphere.nc").sel(time=time_slice,lat = lat_slice,lon = lon_slice)
    # 设置画布
    proj    =  ccrs.PlateCarree()
    fig1    =  plt.figure(figsize=(15,18))
    spec1   =  fig1.add_gridspec(nrows=1,ncols=1)

    j = 0
    name   =  ["CGCM - AGCM"]

    for col in range(1):
        ax = fig1.add_subplot(spec1[0,col])

        # 设置坐标轴
        ax.set_xticks(np.arange(70,131,20))
        ax.set_xticklabels(x_tick_labels,fontsize=30)
        ax.set_yticks(y_tick)
        ax.set_yticklabels(y_label,fontsize=30)

        ax.set_title(name[j],fontsize=45,loc='left')

        clev  =  np.array([-10,-6,-3,-2,-1,0,1,2,3,6,10])
        cf   = ax.contourf(f0.lon.values, f0.time.values,1.1*(model[1] - model[0]), clev, cmap=newcmp, extend='both')
        clev  =  np.array([-10,-6,-3,-2,-1,1,2,3,6,10])
        cs   = ax.contour(f0.lon.values,  f0.time.values,1.1*(model[1] - model[0]), clev, colors='k', linewidths=1)


        j += 1
    
    fig1.subplots_adjust(top=0.8) 
    cbar_ax = fig1.add_axes([0.2, 0.05, 0.6, 0.03]) 
    cb  =  fig1.colorbar(cf, cax=cbar_ax, shrink=0.1, pad=0.01, orientation='horizontal')
    cb.ax.set_xticks(np.array([-10,-6,-3,-2,-1,0,1,2,3,6,10],dtype=int))
    cb.ax.tick_params(labelsize=22)
    save_fig(path_out=path_out,file_out=filename)



def main():
    model = lon_avg_wind_925()
    paint_model_hov(model,path_out="/home/sun/paint/b1850_exp/f2000_ensemble/",filename="hov_10-20_con_agcm_cgcm_925wind.pdf")
    paint_model_hov_diff(model,path_out="/home/sun/paint/b1850_exp/f2000_ensemble/",filename="hov_10-20_con_agcm_cgcm_diff_925wind.pdf")


if __name__ == "__main__":
    main()