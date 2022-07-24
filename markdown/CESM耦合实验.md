---
title: CESM耦合实验
date: 2022-05-24 09:48:18
tags: CESM
---

## test B1850

```
./create_newcase --case test_b1850 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850
./xmlchange NTASKS=-12 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
```

<font color=#FF000 >编译过程中报错，显示缺少启动文件，这里我手动把文件都下载下来之后再次编译试试</font>

## test B1850-2

```
./create_newcase --case test_b1850_2 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_2
./xmlchange NTASKS=-12 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
```



**编译过程报错**

[![-2022-05-24-104302.png](https://z4a.net/images/2022/05/24/-2022-05-24-104302.png)](https://z4a.net/image/2wphPL)



<font color=green size=10 face="幼圆">debug</font>

<font size=6>参考</font> 

[CESM2.1.3 build failed for B1850,about lapack and blas | DiscussCESM Forums (ucar.edu)](https://bb.cgd.ucar.edu/cesm/threads/cesm2-1-3-build-failed-for-b1850-about-lapack-and-blas.6288/)

<font color=red>修改</font>

在config_compliers里加了一句

```xml
-L/public1/home/wgx/intel/oneapi/mkl/2021.3.0/lib/intel64 -lmkl_rt
```



## test_b1850_3

```
./create_newcase --case test_b1850_3 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_3
./xmlchange NTASKS=-12 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
```

<font color=red size=6 face="kaiti">解决!</font>



<font size=6.5>下载完inputdata之后测试运行</font>

## test_b1850_4

```
./create_newcase --case test_b1850_4 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_4
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
```



## test_b1850_5

```
./create_newcase --case test_b1850_5 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_5
./xmlchange NTASKS=-28
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup

```



结果报错，大致如下

>ERROR: WW3 EXTCDE abort



## test_b1850_6

```shell
./create_newcase --case test_b1850_6 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_6
./xmlchange NTASKS=-30
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

这里我在sbatch1文件里面调大了节点数报错，看来还是要跟设置里面的相一致才行



## test_b1850_7

```
./create_newcase --case test_b1850_7 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_7
./xmlchange NTASKS=-30
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

报错



## test_b1850_8

```
./create_newcase --case test_b1850_8 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_8
./xmlchange NTASKS=-24
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

额跑起来了。。（卧槽为什么！）



## test_b1850_10

```
./create_newcase --case test_b1850_10 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_10
./xmlchange NTASKS=-24
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

报错



## test_b1850_11

```
./create_newcase --case test_b1850_12 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_12
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

出现的问题：空转



## test_b1850_13

```
./create_newcase --case test_b1850_13 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_13
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```





## test_b1850_14

```
./create_newcase --case test_b1850_14 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_14
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

报错，会不会是提交的太多了？



## test_b1850_15

```
./create_newcase --case test_b1850_16 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_16
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

报错



<font color=red>这次改了config_compliers再试试</font>

## test_b1850_17

```
./create_newcase --case test_b1850_17 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_17
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .
```

<font color=red>至此成功了</font>

```
./create_newcase --case test_b1850_18 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_18
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .
```

# test_b1850_19 lym服务器测试

```
./create_newcase --case test_b1850_21 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_21
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/test_b1850_17/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/test_b1850_17/sbatch1.sh .
```







# 更改海陆分布实验记录

### 无印度大陆实验,这里没有改温盐初始场

<font size=5.5>制作mask以及bathy文件</font>

```python
import numpy as np
import xarray as xr


bathy  =  np.fromfile("/home/sun/data/cesm/topography_20161215.ieeei4",dtype='>i4')
f1     =  xr.open_dataset('/home/sun/data/cesm/gx1v7_151008.nc')

lat_extent1  =  [8,23]
lon_extent1  =  [65,90]


new_mask   =  f1.grid_imask.data
new_bathy  =  bathy
new_lat    =  f1.grid_center_lat.data
new_lon    =  f1.grid_center_lon.data
import math

for i in range(0,len(f1.grid_imask)):
    if (f1.grid_center_lat.data[i] > math.radians(lat_extent1[0]) and f1.grid_center_lat.data[i] < math.radians(lat_extent1[1])) and (f1.grid_center_lon.data[i] > math.radians(lon_extent1[0]) and f1.grid_center_lon.data[i] < math.radians(lon_extent1[1])):
        new_mask[i]  =  1
        new_bathy[i] =  10
```

<font size=5.5>制作domain文件</font>

```shell
source ~/swh/esmf.sh
cd /public1/home/wgx/swh/cesm2.1.3/cime/tools/mapping/gen_mapping_files
./gen_cesm_maps.sh --serial -fatm /public1/home/wgx/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn /public1/home/wgx/swh/data/domain/gx1v7_220605_indian.nc -nocn gx1v7_noindian --nogridcheck
cd ../gen_domain_files/
./gen_domain -m ../gen_mapping_files/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc -o gx1v7_noindian -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

<font size=5.5>实验流程(1)</font>

```shell
./create_newcase --case b1850_noindian --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/user_nl_docn .
cp ../replace_india8/user_nl_cice .
cp ../replace_india8/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>失败了，状况是空转，不报错也不输出文件</font>

<font size=5.5>实验流程(2) 采用了新的initial condition文件试一试，制作的过程中使用的是240*122880的</font>

```shell
./create_newcase --case b1850_noindian2 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian2
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian/user_nl_cam .
cp ../b1850_noindian/user_nl_cice .
cp ../b1850_noindian/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font size=5.5>实验流程(3) 采用了新的initial condition文件试一试，制作的过程中全给换成3</font>

```shell
./create_newcase --case b1850_noindian3 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian3
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian2/user_nl_cam .
cp ../b1850_noindian2/user_nl_cice .
cp ../b1850_noindian2/user_nl_pop .
cp ../b1850_noindian2/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font size=5.5>实验流程(4) 测试新的ic文件</font>

制作流程

```python
import numpy as np
import math

data  =  np.fromfile("/home/sun/data/cesm/ts_PHC2_jan_ic_gx1v6_20090205.ieeer8", dtype='>f8')

import xarray as xr
bathy  =  np.fromfile("/home/sun/data/cesm/topography_20161215.ieeei4",dtype='>i4')
f1     =  xr.open_dataset('/home/sun/data/cesm/gx1v7_151008.nc')

ts     =  data.reshape((2,60,384,320))
bathy2 =  bathy.reshape((384,320))
lat    =  f1.grid_center_lat.data.reshape((384,320))
lon    =  f1.grid_center_lon.data.reshape((384,320))

lat_extent1  =  [8,23]
lon_extent1  =  [65,90]


new_lat    =  f1.grid_center_lat.data
new_lon    =  f1.grid_center_lon.data
import math

for n in range(2):
    for x in range(384):
        for y in range(320):
            if (lat[x,y] > math.radians(lat_extent1[0]) and lat[x,y] < math.radians(lat_extent1[1])) and (lon[x,y] > math.radians(lon_extent1[0]) and lon[x,y] < math.radians(lon_extent1[1])):
                bathy2[x,y] =  1
                ts[n,0,x,y] =  30

result_bathy  =  bathy2.reshape(bathy.shape)
result_ts     =  ts.reshape(data.shape)

result_bathy.tofile("/home/sun/data/cesm/topography_220605_indian_2.ieeei4")
result_ts.tofile("/home/sun/data/cesm/ts_noindian_220605.ieeer8")
```



```shell
./create_newcase --case b1850_noindian4 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian4
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian3/user_nl_cam .
cp ../b1850_noindian3/user_nl_cice .
cp ../b1850_noindian3/user_nl_pop .
cp ../b1850_noindian3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>还是空转</font>

试试什么都不改呢？

```
./create_newcase --case b1850_noindian5 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian5
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian3/user_nl_cam .
cp ../b1850_noindian3/sbatch1.sh .
```



<font size=5.5>实验流程(5) 测试ncl制作的ic文件</font>

ncl脚本如下

```ncl
begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    ts_in     =  "/home/sun/data/cesm/ts_PHC2_jan_ic_gx1v6_20090205.ieeer8"
    file0     =  "/home/sun/data/cesm/gx1v7_151008.nc"

    latlonf   =  addfile(file0,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon

    pi        =  3.141592653

    ; range
    lat1      =  0.13962634015954636
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966

    setfileoption("bin","ReadByteOrder","BigEndian")
    tracer = fbindirread (ts_in, 0, -1, "double")
    tracer := reshape(tracer,(/2,60,384*320/))


    do n=0,1
        do ll=0,59
            do dim3=0,(384*320)-1
                if (lat(dim3) .gt. lat1 .and. lat(dim3) .lt. lat2 .and. lon(dim3) .gt. lon1 .and. lon(dim3) .lt. lon2) then
                    tracer(n,0,dim3)  =  30
                end if
            end do
        end do
    end do

    ts_out    =    "/home/sun/data/cesm/ts_noindian_0605.ieeer8"
   ; sys       =    systemfunc("rm "+ts_out)
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite (ts_out, tracer)



end

begin
    bathy_in  =  "/home/sun/data/cesm/topography_20161215.ieeei4"
    file0     =  "/home/sun/data/cesm/gx1v7_151008.nc"
    setfileoption("bin","ReadByteOrder","BigEndian")
    bath = fbindirread (bathy_in, 0, -1, "integer")

    latlonf   =  addfile(file0,"r")
    lat       =  latlonf->grid_center_lat
    lon       =  latlonf->grid_center_lon

    pi        =  3.141592653

    ; range
    lat1      =  0.13962634015954636
    lat2      =  0.4014257279586958
    lon1      =  1.1344640137963142
    lon2      =  1.5707963267948966


    do dim3=0,(384*320)-1
        if (lat(dim3) .gt. lat1 .and. lat(dim3) .lt. lat2 .and. lon(dim3) .gt. lon1 .and. lon(dim3) .lt. lon2) then
            bath(dim3)  =  1
        end if
    end do

    bathy_out    =    "/home/sun/data/cesm/topography_noindian_220605.ieeei4"
    setfileoption("bin","WriteByteOrder","BigEndian")
    fbindirwrite(bathy_out, bath)


end
```

```shell
./create_newcase --case b1850_noindian6 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian6
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian5/user_nl_cam .
cp ../b1850_noindian5/user_nl_cice .
cp ../b1850_noindian5/user_nl_pop .
cp ../b1850_noindian5/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>运行出了一天的数据然后爆掉了</font>

这次我在制作文件的过程中设置成了10层

```
./create_newcase --case b1850_noindian8 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian8
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian7/user_nl_cam .
cp ../b1850_noindian7/user_nl_cice .
cp ../b1850_noindian7/user_nl_pop .
cp ../b1850_noindian7/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>运行出了一天的数据然后爆掉了</font>

<font size=5.5>实验流程(6) 初始ic设置成0</font>

```
./create_newcase --case b1850_noindian9 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian9
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian7/user_nl_cam .
cp ../b1850_noindian7/user_nl_cice .
cp ../b1850_noindian7/user_nl_pop .
cp ../b1850_noindian7/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font size=5.5>实验流程(6) 初始ic设置成25,35</font>

```
./create_newcase --case b1850_noindian10 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian10
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian9/user_nl_cam .
cp ../b1850_noindian9/user_nl_cice .
cp ../b1850_noindian9/user_nl_pop .
cp ../b1850_noindian9/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font size=5.5>实验流程(7) 初始ic设置成纬向平均的</font>

```shell
./create_newcase --case b1850_noindian11 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian11
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian9/user_nl_cam .
cp ../b1850_noindian9/user_nl_cice .
cp ../b1850_noindian9/user_nl_pop .
cp ../b1850_noindian9/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

```
./create_newcase --case b1850_noindian12 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian12
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian9/user_nl_cam .
cp ../b1850_noindian9/user_nl_cice .
cp ../b1850_noindian9/user_nl_pop .
cp ../b1850_noindian9/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

```
./create_newcase --case b1850_noindian13 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian13
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian9/user_nl_cam .
cp ../b1850_noindian9/user_nl_cice .
cp ../b1850_noindian9/user_nl_pop .
cp ../b1850_noindian9/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red size=5>测试一下是不是domain的问题</font>

```
./create_newcase --case b1850_noindian14 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian14
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/user_nl_docn .
cp ../replace_india8/user_nl_cice .
cp ../replace_india8/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

没问题

<font size=5.5>实验流程(8) 更改dt_count</font>

```
./create_newcase --case b1850_noindian15 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian15
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian13/user_nl_cam .
cp ../b1850_noindian13/user_nl_cice .
cp ../b1850_noindian13/user_nl_pop .
cp ../b1850_noindian13/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

```
./create_newcase --case b1850_noindian16 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian16
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian15/user_nl_cam .
cp ../b1850_noindian15/user_nl_cice .
cp ../b1850_noindian15/user_nl_pop .
cp ../b1850_noindian15/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

dt_count改成48 结果：不行

<font size=5.5>实验流程(9) 更改ic文件，这里设置成50，以及把init_ts_file_fmt改成了‘bin’</font>

```
./create_newcase --case b1850_noindian17 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian17
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian15/user_nl_cam .
cp ../b1850_noindian15/user_nl_cice .
cp ../b1850_noindian15/user_nl_pop .
cp ../b1850_noindian15/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>注意。修改了bin会报错的</font>

<font size=5.5>实验流程(10) 更改ic文件，这里设置成50</font>

```
./create_newcase --case b1850_noindian18 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian18
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../b1850_noindian17/user_nl_cam .
cp ../b1850_noindian17/user_nl_cice .
cp ../b1850_noindian17/user_nl_pop .
cp ../b1850_noindian17/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

失败，问题同之前一样，跑几步就坏了

<font size=5.5>实验流程(11) 更改ic文件，水深设置为1，使用possion差值</font>

```
./create_newcase --case b1850_noindian20 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi2
cd b1850_noindian20
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian18/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian18/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian18/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian18/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./case.build
```

<font color=red>跑到第6个月炸了</font>

<font size=5.5>实验流程(11) 更改ic文件，水深设置为10，使用possion差值</font>

```
./create_newcase --case b1850_noindian21 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi2
cd b1850_noindian21
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./case.build
```

<font color=red>跑到第6个月炸了</font>

<font size=5.5>实验流程(11) 更改ic文件，水深设置为10，使用possion差值，更改dt</font>

```
./create_newcase --case b1850_noindian22 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi2
cd b1850_noindian22
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./case.build
```

```
./create_newcase --case b1850_noindian23 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi2
cd b1850_noindian23
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./case.build
```

<font size=5.5>实验流程(12) 更改ic文件，水深设置为10，使用possion差值，对应位置设置缺测，更改dt,</font>

```
./create_newcase --case b1850_noindian24 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi2
cd b1850_noindian24
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian20/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./case.build
```

<font size=5.5>实验流程(12) 更改ic文件，水深设置为10，使用possion差值，对应位置设置缺测，更改dt,更改source code</font>

```
./create_newcase --case b1850_noindian25 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian25
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>不可以</font>

<font size=5.5>实验流程(13) 更改ic文件，水深设置为全60</font>

```
./create_newcase --case b1850_noindian_all60 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian_all60
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian24/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

```
./create_newcase --case b1850_noindian_all60_2 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian_all60_2
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

<font color=red>报错信息</font>

```
ice_therm_mushy solver failure: istep1, my_task, i, j:    11843522         434
           9           2
 ice_therm_mushy solver failure
 ERROR: ice_therm_mushy solver failure
  -110121000.000000     
           2  0.000000000000000E+000  0.000000000000000E+000
  -110121000.000000     
           3  0.000000000000000E+000  0.000000000000000E+000
  -110121000.000000     
           1  -21.1051998283774                          NaN
   12.4655936891537                          NaN  5.699146249043224E-002
  -332135974.581950     
           2  -17.7832370429661                          NaN
   11.2613850846571                          NaN  5.709181758304912E-002
  -325250777.029684     
           3  -14.6544324271349                          NaN
   10.2180123301685                          NaN  5.808535338611050E-002
  -318517942.730343     
           4  -11.7124819210732                          NaN
   9.39737922714830                          NaN  6.071044956516562E-002
  -311700283.300608     
           5  -8.84978412027958                          NaN
   9.15852212423978                          NaN  6.877345005308819E-002
  -303453847.213418     
           6  -5.46551325949210                          NaN
   10.1483004972088                          NaN  0.110623852148638     
  -284068153.324988     
           7  -2.43047877575834                          NaN
   13.5625705452904                          NaN  0.315521731784365     
  -215826377.182280     
           8  -1.58833611678078                          NaN
   20.6067430246963                          NaN  0.722651785775100     
  -90430565.5499296     
```

```
./create_newcase --case b1850_noindian_all60_3 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian_all60_3
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_2/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_2/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_2/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_2/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```

```
# 这里尝试不改动极区的温盐，只改热带的
./create_newcase --case b1850_noindian_all60_5 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian_all60_5
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_4/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_4/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_4/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_4/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_3/SourceMods/src.cice/* ./SourceMods/src.cice/
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange ICE_NCPL=12

# 显示couple的问题，看来不能只改一个NCPL
```

https://xenforo.cgd.ucar.edu/cesm/threads/faq-cice-thermodynamic-convergence-errors.4202/



```
# 这里尝试不改动极区的温盐，只改热带的
./create_newcase --case b1850_noindian_all60_6 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_noindian_all60_6
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_3/SourceMods/src.cice/* ./SourceMods/src.cice/
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'


# 显示couple的问题，看来不能只改一个NCPL
```



### 关于积分不稳定问题的几个测试

1. 对bathy也进行possion插值
2. 保留原始的海盆，不动bathy，对温盐进行插值
3. 保留原始的海盆，不动bathy，对温盐使用纬向平均
4. 温盐场不变，对原本的海域进行修改bathy值
5. 不对bathy进行插值，在那片区域全部设为统一kmt
6. 统一海盆+possion温盐场
7. 统一海盆（不更改海陆分布）+possion温盐场
8. 同4，但改动范围更大
9. 同8，+possion温盐场
10. 设立一条缝式的KMT+POSSION温盐场
11. 更大范围给一个区域的KMT
12. 是否是海陆边界位置交界处的问题呢？设计一个实验，不动海陆分布但是选取一个海陆交界处更改kmt

<font size=6>1.</font>

```
./create_newcase --case test_ts1 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts1
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../test_tc1/user_nl_cam .
cp ../test_tc1/user_nl_cice .
cp ../test_tc1/user_nl_pop .
cp ../test_tc1/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
```



<font size=6>2.</font>

```
# ncl 处理如下
poisson_grid_fill( tracer(:,:,:,:), is_cyclic, guess, nscan, eps, relc, opt) 
tracer(:,:,0:1,:)=-99
tracer(:,:,382:383,:)=-99

# CESM
./create_newcase --case test_ts2 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts2
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .

# 成功输出数据
```

<font size=6>3</font>

```
# ncl 处理如下
    do dim3=100,200
        do dim4=0,319
            if ismissing(tracer(0,0,dim3,dim4)) then
                continue
            else
                tracer(0,0,dim3,dim4) = dim_avg_n(tracer(0,0,dim3,:), 0)
                tracer(1,0,dim3,dim4) = dim_avg_n(tracer(1,0,dim3,:), 0)
            end if
        end do
    end do
    
# CESM
./create_newcase --case test_ts3 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts3
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .
```

<font size=6>4</font>

```
#ncl 修改
bathy(100:105,90:95)  =  20

# CESM 注：温盐场原始值
./create_newcase --case test_ts4 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts4
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .
```

<font size=6>5</font>

```
./create_newcase --case test_ts5 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts5
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_noindian.220615.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_noindian.220615.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_noindian.220615.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_noindian.220615.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_aave.220615.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_blin.220615.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_patc.220615.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_noindian_TO_fv09_125_aave.220615.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_noindian_TO_fv09_125_aave.220615.nc'

#报错  MARBLE ERROR
```



<font size=6>6</font>

```
./create_newcase --case test_ts6 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts6
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/b1850_noindian_all60_5/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'

#报错  MARBLE ERROR
```

<font size=6>7</font>

```
./create_newcase --case test_ts7 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts7
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ~/swh/cesm2.1.3/cime/scripts/test_ts6/user_nl_cam .
cp ~/swh/cesm2.1.3/cime/scripts/test_ts6/user_nl_cice .
cp ~/swh/cesm2.1.3/cime/scripts/test_ts6/user_nl_pop .
cp ~/swh/cesm2.1.3/cime/scripts/test_ts6/sbatch1.sh .

#报错  MARBLE ERROR
```

<font size=6>8</font>

```
#ncl 修改
bathy(100:150,90:120)  =  5

# CESM 注：温盐场用的原始的
./create_newcase --case test_ts8 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts8
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_ts4/user_nl_cam .
cp ../test_ts4/sbatch1.sh .
cp ../test_ts6/user_nl_cice .
cp ../test_ts4/user_nl_pop .
```

<font size=6>9</font>

```
#ncl 修改
bathy(100:150,90:120)  =  5

# CESM 注：温盐场用的原始的
./create_newcase --case test_ts9 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts9
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_ts8/user_nl_cam .
cp ../test_ts8/sbatch1.sh .
cp ../test_ts8/user_nl_cice .
cp ../test_ts8/user_nl_pop .
```



<font size=6>10</font>

```
#ncl 修改
bathy(100:150,120)  =  5

# CESM 注：温盐场用的原始的
./create_newcase --case test_ts10 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts10
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_ts8/user_nl_cam .
cp ../test_ts8/sbatch1.sh .
cp ../test_ts8/user_nl_cice .
cp ../test_ts8/user_nl_pop .
```

<font size=6>11</font>

```
./create_newcase --case test_ts11 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_ts11
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../test_ts5/user_nl_cam .
cp ../test_ts5/user_nl_cice .
cp ../test_ts5/user_nl_pop .
cp ../test_ts5/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220605.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220605.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220605.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220605.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220605.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220605.nc'

```



#### 小结：

2无报错，因此即便温盐初始场没有缺测也是可以的

3无报错，对部分区域修改温盐场环流是可以的

4我取了一个正方形区域重新设置KMT，没有报错

5报错，MARBLE

6统一海盆会报错，MARBLE

7报错



# 重新制作印度大陆的map文件

## 制作domain文件 这次把陆地去除干净了

```
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v7_220608_indian.nc -nocn gx1v7_noindian --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1v7_noindian_TO_fv09_125_aave.220608.nc -o gx1v7_noindian -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

## 实验

重新制作了kmt文件 topography_noindian_220608.ieeei4 温盐场使用possion插值后的结果

```
./create_newcase --case b1850_indian1 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_indian1
./xmlchange NTASKS=-10
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../test_ts5/user_nl_cam .
cp ../test_ts5/user_nl_cice .
cp ../test_ts5/user_nl_pop .
cp ../test_ts5/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220608.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noindian.220608.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220608.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noindian.220608.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_aave.220608.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_blin.220608.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noindian_patc.220608.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220608.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noindian_TO_fv09_125_aave.220608.nc'
```









## 控制实验

```shell
./create_newcase --case b1850_control_220608 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_control_220608
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../f2000_control_220513/user_nl_cam .
cp ../f2000_control_220513/sbatch1.sh .

# 不知道为什么空转
```

```
./create_newcase --case test_b1850_19 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd test_b1850_19
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .

#这次倒是输出值了
```

<font color=red>重新测试一下control</font>

```
./create_newcase --case b1850_control_220608_2 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_control_220608_2
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../test_b1850_17/user_nl_cam .
cp ../test_b1850_17/sbatch1.sh .
```

# 控制实验



# 地形实验

## 全球1m陆地实验(lym)

```shell
./create_newcase --case b1850_global_1m_3 --res f09_g17 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850_global_1m_3
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../10m_all/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/test_b1850_17/sbatch1.sh .
```

## 更换格点后1m陆地实验(lym)

```
./create_newcase --case b1850_global_1m_4_220614 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global_1m_4_220614
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850m_no_indian_4_220612/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.1.3/cime/scripts/b1850_global_1m_3/user_nl_cam .
./case.build --skip-provenance-check
```

## 中途断掉了，这里重新branch一下，把核数放多些

```shell
./create_newcase --case b1850_global_1m_220620 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global_1m_220620
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_global_1m_4_220614
./xmlchange RUN_REFDATE=0021-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=3
./xmlchange RESUBMIT=60
./xmlchange REST_N=3
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_4_220614/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_4_220614/sbatch1.sh .
./case.build --skip-provenance-check

cp b1850_global_1m_4_220614/run/*.r.* b1850_global_1m_220620/run/
cp b1850_global_1m_4_220614/run/*.rs.* b1850_global_1m_220620/run/
cp b1850_global_1m_4_220614/run/*rpo* b1850_global_1m_220620/run/
```



# B1850MOM的实验

## 测试

### case1

```
./create_newcase --case b1850m_test1 --res f09_g16 --compset B1850 --run-unsupported --compiler intel --mach oneapi
cd b1850m_test1
./xmlchange NTASKS=-18
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
```

<font color=red size=6>2022-6-10 MOM6测试已跑通</font>

### case2 在lym服务器上的测试

```
./create_newcase --case b1850m_test2_220614 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test2_220614
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=5
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850m_no_indian_4_220612/sbatch1.sh .
./case.build --skip-provenance-check
```





## 对MOM6输入文件的测试

<font color=brown size=5.5>在新建case中，发现MOM6所需要的外缘文件有：</font>

ocean_hgrid.nc  ocean_topog.nc  ocean_vgrid.nc  WOA05_pottemp_salt.nc

### 关于外源文件的内容

ocean_hgrid.nc

![-2022-06-10-115540.png](https://z4a.net/images/2022/06/10/-2022-06-10-115540.png)



ocean_topog.nc

![-2022-06-10-115711.png](https://z4a.net/images/2022/06/10/-2022-06-10-115711.png)

<img src="https://z4a.net/images/2022/06/10/-2022-06-10-133038.png" alt="-2022-06-10-133038.png" style="zoom:80%;" />



ocean_vgrid.nc

![-2022-06-10-115637.png](https://z4a.net/images/2022/06/10/-2022-06-10-115637.png)

<font size=5 color=red>这里全部的加起来是5500，所以我想应该是每一层之间的厚度(m)</font>

WOA05_pottemp_salt.nc

![-2022-06-10-115726.png](https://z4a.net/images/2022/06/10/-2022-06-10-115726.png)

<img src="https://z4a.net/images/2022/06/10/-2022-06-10-133445.png" alt="-2022-06-10-133445.png" style="zoom:80%;" />

## MOM6中修改海陆分布测试

### depth文件与ic文件的制作

<font size=5.5>在这里面深度给的是纬向平均值，IC使用的POSSION插值，这可能引入问题</font>

<font size=5.5>脚本  cal-change_topo_ts_mom6.ncl</font>

<font size=5.5 color=red>实验（1）不改变其他，替用possion插值后的结果温盐场</font>

```
./create_newcase --case b1850m_test_possionic --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_possionic
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_control_220608_2/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_control_220608_2/sbatch1.sh .
./case.build --skip-provenance-check
```

<font color=red>可以</font>



### ESMF mapping的制作

```
cd /public1/home/wgx/swh/cesm2.1.3/cime/tools/mapping/gen_mapping_files
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v6_220610_indian.nc -nocn gx1v6_noindian --nogridcheck
cd ../gen_domain_files
./gen_domain -m ../gen_mapping_files/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc -o gx1v6_noindian -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v6/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```



## 正式实验

```
./create_newcase --case b1850m_test_indian1 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_indian1
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian22/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_control_220608_2/sbatch1.sh .
cp ../b1850m_test_possionic/user_nl_mom .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

<font size=5.5 color=red>报错，报错原因说是domain文件对不上</font>

```
./create_newcase --case b1850m_test_indian2 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_indian2
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_test_indian1/user_nl_cam .
cp ../b1850m_test_indian1/sbatch1.sh .
cp ../b1850m_test_indian1/user_nl_mom .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

<font color=red>查一下是不是海冰的问题</font>

这里我重新制作了海冰的kmt文件，再试试

```
./create_newcase --case b1850m_test_indian3 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_indian3
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian22/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian22/user_nl_cice .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_control_220608_2/sbatch1.sh .
cp ../b1850m_test_possionic/user_nl_mom .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

这里我重新制作了海冰的kmt文件*2，再试试

```
./create_newcase --case b1850m_test_indian4 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_indian4
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_noindian22/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.1.3/cime/scripts/b1850_control_220608_2/sbatch1.sh .
cp ../b1850m_test_indian1/user_nl_mom .
cp ../b1850m_test_indian3/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

成功了

```
./create_newcase --case b1850m_test_indian5 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_test_indian5
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_test_indian4/user_nl_cam .
cp ../b1850m_test_indian4/sbatch1.sh .
cp ../b1850m_test_indian4/user_nl_mom .
cp ../b1850m_test_indian4/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```





<font size=6 color=red>正式实验</font>

```
./create_newcase --case b1850m_no_indian_2_220611 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_no_indian_2_220611
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_test_indian4/user_nl_cam .
cp ../b1850m_test_indian4/sbatch1.sh .
cp ../b1850m_test_indian4/user_nl_mom .
cp ../b1850m_test_indian4/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

到第7年崩掉了，这里尝试对地形进行possion插值之后再试试

```
./create_newcase --case b1850m_no_indian_2_220612 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_no_indian_2_220612
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_no_indian_2_220611/user_nl_cam .
cp ../b1850m_no_indian_2_220611/sbatch1.sh .
cp ../b1850m_no_indian_2_220611/user_nl_mom .
cp ../b1850m_no_indian_2_220611/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

这里尝试对地形进行possion插值之后再试试，加上对海冰地形的possion插值

```
./create_newcase --case b1850m_no_indian_5_220612 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_no_indian_5_220612
./xmlchange NTASKS=-48
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_no_indian_4_220612/user_nl_cam .
cp ../b1850m_no_indian_4_220612/sbatch1.sh .
cp ../b1850m_no_indian_4_220612/user_nl_mom .
cp ../b1850m_no_indian_4_220612/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v6_noindian.220610.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v6_noindian.220610.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_aave.220610.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_blin.220610.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v6_noindian_patc.220610.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v6/map_gx1v6_noindian_TO_fv09_125_aave.220610.nc'
./case.build --skip-provenance-check
```

第8年断了

## 更换MOM6的格点

<font color=red>f09_t061</font>

```
./create_newcase --case b1850m_control3_220617 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m_control3_220617
./xmlchange NTASKS=-50
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../b1850m_control2_220616/sbatch1.sh .
./case.build --skip-provenance-check
```





## 查找资料

### MOM6中的land-sea mask

[mom_grid_initialize module reference — MOM6 0.2a3 documentation](https://mom6.readthedocs.io/en/main/api/generated/modules/mom_grid_initialize.html#detamom-grid-initialize)

> initialize_masks sets up land masks based on the depth field. The one argument is the minimum ocean depth. Depths that are less than this are interpreted as land points.
>
> 

[MOM6: mom_state_initialization Module Reference (ncar.github.io)](https://ncar.github.io/MOM6/APIs/namespacemom__state__initialization.html)



# B1850MOM TX格点

## 前期准备

SCRIP文件：

reshape参数 458 540

<font color=blue>inputdata</font>

```
ocean_hgrid = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/ocean_hgrid_180829.nc
ocean_vgrid1 = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/vgrid_65L_20200626.nc
ocean_topog = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/ocean_topog_200701.nc
tempsalt = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/woa18_04_initial_conditions.nc
saltrestore = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/state_restore_tx0.66v1_20200616.nc
tidal = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/energy_new_t0.66v1_conserve_190315.nc
ocean_channel = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/MOM_channels_global_tx06v1

grid_file = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/grid/horiz_grid_20190315.ieeer8
kmt_file = /public1/home/wgx/swh/cesm2.1.3/inputdata/ocn/mom/tx0.66v1/grid/topography_20190315.ieeei4
```

### 文件信息

[mom6_inputdata](D:\草图\按内容\MOM6输入文件信息\MOM6_inputdata.pdf)

## 制作map文件

```
./gen_cesm_maps.sh --serial -fatm /public1/home/wgx/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn /public1/home/wgx/swh/data/domain/tx0.66v1_SCRIP_noindian_220615.nc -nocn t66_noindian --nogridcheck
cd ../gen_domain_files/
./gen_domain -m ../gen_mapping_files/map_t66_noindian_TO_fv09_125_aave.220615.nc -o t66_noindian -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

## 实验

```shell
./create_newcase --case b1850_tx4_indian_220616 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx4_indian_220616
./xmlchange NTASKS=-40
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=6
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx3_indian_220616/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx3_indian_220616/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx3_indian_220616/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx3_indian_220616/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_noindian.220615.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_noindian.220615.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_noindian.220615.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_noindian.220615.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_aave.220615.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_blin.220615.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_noindian_patc.220615.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_noindian_TO_fv09_125_aave.220615.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_noindian_TO_fv09_125_aave.220615.nc'
./case.build --skip-provenance-check
```



## 制作无海洋性大陆的map文件

```shell
./gen_cesm_maps.sh --serial -fatm /public1/home/wgx/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn /public1/home/wgx/swh/data/domain/tx0.66v1_SCRIP_nomaritime_220623.nc -nocn t66_maritime3 --nogridcheck
cd ../gen_domain_files/
./gen_domain -m ../gen_mapping_files/map_t66_maritime3_TO_fv09_125_aave.220623.nc -o t66_nomaritime -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/tx0.66v1/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

```shell
./create_newcase --case b1850_tx_maritime_220623 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_maritime_220623
./xmlchange NTASKS=-26
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=60
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_nomaritime.220623.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_nomaritime.220623.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_nomaritime.220623.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_nomaritime.220623.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_nomaritime_aave.220623.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_nomaritime_blin.220623.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_nomaritime_patc.220623.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_nomaritime_TO_fv09_125_aave.220623.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_nomaritime_TO_fv09_125_aave.220623.nc'
./case.build --skip-provenance-check
```

## 这次抠的精细，试一试

```
./gen_cesm_maps.sh --serial -fatm /public1/home/wgx/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn /public1/home/wgx/swh/data/domain/tx0.66v1_SCRIP_nomaritime_220623.nc -nocn t66_maritime3 --nogridcheck
cd ../gen_domain_files/
./gen_domain -m ../gen_mapping_files/map_t66_maritime2_TO_fv09_125_aave.220624.nc -o t66_maritime2 -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/tx0.66v1/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```



```shell
./create_newcase --case b1850_tx3_maritime_220624 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx3_maritime_220624
./xmlchange NTASKS=-30
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=75
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_maritime2.220624.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_maritime2.220624.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_maritime2.220624.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_maritime2.220624.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime2_aave.220624.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime2_blin.220624.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime2_patc.220624.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_maritime2_TO_fv09_125_aave.220624.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_maritime2_TO_fv09_125_aave.220624.nc'
./case.build --skip-provenance-check
```



```shell
./create_newcase --case b1850_tx4_maritime_220624 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx4_maritime_220624
./xmlchange NTASKS=-30
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=75
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx2_maritime_220624/user_nl_cice .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_maritime3.220624.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_t66_maritime3.220624.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_maritime3.220624.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.t66_maritime3.220624.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime3_aave.220624.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime3_blin.220624.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_t66_maritime3_patc.220624.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_maritime3_TO_fv09_125_aave.220624.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/tx0.66v1/map_t66_maritime3_TO_fv09_125_aave.220624.nc'
./case.build --skip-provenance-check
```



# 试验记录日志

## global_1m实验

### spin-up

<font color=green>b1850_global_1m_220620</font>     spin文件时间长度21-98年  <font color=red>登记时间20220706</font>



### 正式实验

<font color=green>b1850_global1m_o2_220703</font>    01-18年      <font color=red>2022-7-6</font>



## tx_indian实验

### spin-up

<font color=green>b1850_tx6_indian_220622</font>  41-60   <font color=red>2022-7-6</font>

<font color=green>b1850_tx_indian_220627</font>    01-58   <font color=red>2022-7-6</font>

合计应该够了，可以开始正式实验（220706）



### 正式实验

<font color=green>b1850_tx_indian_o1_220706</font>           <font color=red>2022-7-6提交</font>



## control实验

### spin-up

<font color=green>b1850m_control3_220617</font>  01-52

<font color=green>b1850_control4_220624</font>  53-96

<font color=green>b1850_control_h1_220702</font> 01-03

<font color=red>reach 100years</font>



### 正式实验

<font color=green> b1850_control_o1_220703</font> 



## maritime实验

### spin-up

<font color=green>b1850_tx4_maritime_220624</font> 01-26

<font color=green>b1850_tx_maritime_h1_220629</font> 01-26
