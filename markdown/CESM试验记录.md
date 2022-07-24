---
title: CESM2试验记录
date: 2022-04-05 08:52:08
tags: CESM
comment: 'valine'
categories: model
---

# CESM2试验记录

### 2021/9/1

将中南半岛地形设置为1m

```shell
./create_newcase --case topo_indo_1m_intel --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd topo_indo_1m_intel
./xmlchange NTASKS=-24 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=5
./xmlchange RESUBMIT=4
./xmlchange REST_N=5
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../control/user_nl_cam .
cp ../control/sbatch1.sh .
```



# 控制实验

**wgx**

```shell
./create_newcase --case control_220416 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi2
cd control_220416
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/sbatch1.sh .
```



## 去除高原大地形

### 2021/9/6

1.  在第一次实验中，将青藏高原和伊朗高原都去除，地形设置为200m

[![image-20210906105857784.png](https://z4a.net/images/2022/04/05/image-20210906105857784.png)](https://z4a.net/image/2H9VET)



#### 试验记录

```shell
./create_newcase --case topo_indo_no_plateau --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd topo_indo_no_plateau
./xmlchange NTASKS=-24 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=5
./xmlchange RESUBMIT=4
./xmlchange REST_N=5
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../topo_all_1m_intel2/user_nl_cam .
cp ../topo_all_1m_intel2/sbatch1.sh .
```





# 更改海陆分布实验（一）印度大陆

## 试验记录

```shell
./create_newcase --case india_to_ocean2 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=1
./xmlchange RESUBMIT=3
./case.setup
cp ../topo_all_1m_intel2/user_nl_cam .
cp ../topo_all_1m_intel2/sbatch1.sh .
!除此之外docn，cice均作了相应修改
```

结果：无法正常运行，调查原因显示陆地与海洋的fraction不匹配

<span style='color:red;background:white;font-size:50;font-family:楷体;'>这里寻找其他的办法</span>

### 参考资料

[reource for cesm1.2 paleosimulations](https://www.cesm.ucar.edu/models/paleo/faq/#intro)



## 制作mapping文件

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/file_for_cesm_change_domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/file_for_cesm_change_domain/gx1v6_090205_swh.nc -nocn gx1PT --nogridcheck
```

报错

```shell
./gen_cesm_maps.sh  --serial -fatm ~/swh/file_for_cesm_change_domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/file_for_cesm_change_domain/gx1v6_090205_swh.nc -nocn gx1PT --nogridcheck
```

报错

这里试试使用官方的格点文件排查一下可能的错误

[![image-20220327200136190.png](https://z4a.net/images/2022/04/05/image-20220327200136190.png)](https://z4a.net/image/2H9jiv)

还是不行



调查/public1/home/wgx/swh/cesm2.1.3/cime/tools/mapping/gen_mapping_files下的PET0.RegridWeightGen.Log文件

[![image-20220328094233889.png](https://z4a.net/images/2022/04/05/image-20220328094233889.png)](https://z4a.net/image/2H9yzn)

<font color='red'>显示似乎是NETCDF模块的问题</font>

尝试重新安装ESMF，这里参考知乎上的教程

第二次安装时候的设置

[![qLGp7R.png](https://s1.ax1x.com/2022/04/05/qLGp7R.png)](https://imgtu.com/i/qLGp7R)





以上设置在make地阶段就坏了，这里只是把编译器换成intel的试了试

<font color='red'>使用intel的编译器安装倒是成功了，但还是显示上述问题，看来依然需要在编译的时候出了问题</font>

那就，重装吧

第一次尝试

```shell
export ESMF_NETCDF="split"
export ESMF_NETCDF_INCLUDE=/public1/home/wgx/swh/app/oneapi/netcdf4/include
export ESMF_NETCDF_LIBPATH=/public1/home/wgx/swh/app/oneapi/netcdf4/lib
# export ESMF_NETCDF_LIBS="-lnetcdf -lnetcdff"
```



<font color='red'>domain文件制作成功，接下来放进模式中试试</font>

**制作domain文件流程记录**

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/file_for_cesm_change_domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/file_for_cesm_change_domain/gx1v7_151008_swh.nc -nocn gx1PT --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1PT_TO_fv09_125_aave.220329.nc -o gx1PT -l fv09_125
```



**第一次尝试**

```shell
./create_newcase --case change_domain_1 --res f09_g16 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_1
./xmlchange NTASKS=-20 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test1/user_nl_cam .
cp ../f2000_test1/sbatch1.sh .
```

```
./create_newcase --case change_domain_2 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_2
./xmlchange NTASKS=-20 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test1/user_nl_cam .
cp ../f2000_test1/sbatch1.sh .
```

```
./create_newcase --case change_domain_3 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_3
./xmlchange NTASKS=-20 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
```

**这里我对clm的namelist进行了修改，但是随后在编译的过程中出现了报错**

```
err=ERROR : CLM build-namelist::CLMBuildNamelist::setup_logic_lnd_frac() : Can NOT set both -lnd_frac option (set via LND_DOMAIN_PATH/LND_DOMAIN_FILE env variables) AND fatmlndfrac on namelist

```

这里使用xmlchange对lnd吃进去的domain文件进行了修改，但是cpl的mapping文件却无法修改成功，只在user_nl_cpl里修改会报错

这里编译成功了，但是运行的过程中报错了，明天试试修改ATM_DOMAIN_FILE

```shell
./create_newcase --case change_domain_4 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_4
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
```

```shell
./create_newcase --case change_domain_5 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_5
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_aave.220329.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_blin.220329.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_patc.220329.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
```

<font color='red'>结果是报错：</font>

 ERROR: surfdata/fatmgrid lon/lat mismatch error  5.684341886080801E-014

这里我换个组件试试

```
./create_newcase --case change_domain_6 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd change_domain_6
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_aave.220329.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_blin.220329.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_patc.220329.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
```

这里我尝试修改源代码，增大lat/lon的判定范围试试

```
./create_newcase --case change_domain_7 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd change_domain_7
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1PT.220329.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT.220329.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_aave.220329.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_blin.220329.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1PT_patc.220329.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_TO_fv09_125_aave.220329.nc'
cp ../change_domain_6/user_nl_docn .
cp ../change_domain_6/user_nl_cice .

```

还是他妈的报错，这里准备重新自己制作一个不修改海陆分布的试试，看看问题出在哪

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/file_for_cesm_change_domain/fv0.9x1.25_141008.nc -natm fv09_125_1 -focn ~/swh/file_for_cesm_change_domain/gx1v7_151008.nc -nocn gx1PT_1
```

```
./create_newcase --case change_domain_8 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd change_domain_8
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_1_gx1PT_1.220331.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_1_gx1PT_1.220331.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT_1.220331.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT_1.220331.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_aave.220331.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_blin.220331.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_patc.220331.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_1_TO_fv09_125_1_aave.220331.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_1_TO_fv09_125_1_aave.220331.nc'
cp ../change_domain_6/user_nl_docn .
cp ../change_domain_6/user_nl_cice .
```

尝试控制实验

```
./create_newcase --case change_domain_8 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd change_domain_8
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_1_gx1PT_1.220331.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_1_gx1PT_1.220331.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT_1.220331.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1PT_1.220331.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_aave.220331.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_blin.220331.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_1_TO_gx1PT_1_patc.220331.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_1_TO_fv09_125_1_aave.220331.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1PT_1_TO_fv09_125_1_aave.220331.nc'
```

<font color='red'>结果成功了</font>





### 2022-4-1再次尝试

**制作domain文件**

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/data/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/gx1v7_151008.nc -nocn gx1pt --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1pt_TO_fv09_125_aave.220401.nc -o gx1pt -l fv09_125 -p 2
cp domain.lnd.fv09_125_gx1pt.220401.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cp domain.ocn.gx1pt.220401.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/

```

**尝试**

```
./create_newcase --case change_domain_10 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_10
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_TO_fv09_125_aave.220401.nc'
cp ../change_domain_6/user_nl_docn .
cp ../change_domain_6/user_nl_cice .

```

**去除印度大陆**

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/data/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/gx1v7_151008_swh.nc -nocn gx1pt_swh --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1pt_swh_TO_fv09_125_aave.220401.nc -o gx1pt_swh -l fv09_125 -p 2
cp domain.lnd.fv09_125_gx1pt_swh.220401.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cp domain.ocn.gx1pt_swh.220401.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp map_gx1pt_swh_TO_fv09_125_* ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp map_fv09_125_TO_gx1pt_swh_* ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

```
./create_newcase --case change_domain_11 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd change_domain_11
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=4
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_test10/user_nl_cam .
cp ../f2000_test10/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
cp ../change_domain_6/user_nl_docn .
cp ../change_domain_6/user_nl_cice .

```

**正式实验**

```
./create_newcase --case replace_india4 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd replace_india4
./xmlchange NTASKS=-16 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=10
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

**正式实验2**

```
./create_newcase --case replace_india5 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd replace_india5
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=1
./xmlchange RESUBMIT=10
./xmlchange REST_N=1
./xmlchange REST_OPTION=nmonths
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

这种反复提交的会报错，我也不知道为什么，只能设置一个一次跑完的了

**正式实验3**

```
./create_newcase --case replace_india8 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd replace_india8
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

### 测试服务器的resubmit问题：使用过程中第二次提交的时候总会有问题

```
./create_newcase --case replace_india7 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd replace_india7
./xmlchange NTASKS=-4 
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=5
./xmlchange RESUBMIT=10
./xmlchange REST_N=10
./xmlchange REST_OPTION=ndays
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

这里我怀疑是mpi的问题，

#### 测试mpi 这里是openmpi服务器自带的

```shell
./create_newcase --case test_resubmit1 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd test_resubmit1
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=5
./xmlchange RESUBMIT=10
./xmlchange REST_N=10
./xmlchange REST_OPTION=ndays
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

会不会是reset文件没跟上呢？

```
./create_newcase --case test_resubmit2 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd test_resubmit2
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=10
./xmlchange RESUBMIT=10
./xmlchange REST_N=5
./xmlchange REST_OPTION=ndays
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```



#### 测试新装的oneapi

```
./create_newcase --case test_oneapi1 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi2
cd test_oneapi1
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india3/user_nl_cam .
cp ../replace_india3/user_nl_docn .
cp ../replace_india3/user_nl_cice .
cp ../replace_india3/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```

# 更改海陆分布实验（二）中南半岛

## 制作domain文件

```
./gen_cesm_maps.sh --serial -fatm ~/swh/data/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/gx1v7_151008_noinch.nc -nocn gx1pt_noinch --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1pt_noinch_TO_fv09_125_aave.220406.nc -o gx1pt_noinch -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```



```shell
./create_newcase --case replace_inch --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi2
cd replace_inch
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
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_noinch.220406.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_noinch.220406.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_noinch.220406.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_noinch.220406.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_aave.220406.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_blin.220406.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_patc.220406.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_noinch_TO_fv09_125_aave.220406.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_noinch_TO_fv09_125_aave.220406.nc'
```



# 更改海陆分布实验（三） 海洋性大陆

**制作domain文件**

```
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v7_220410_nomarinland.nc -nocn gx1pt_nomarinland --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1pt_nomarinland_TO_fv09_125_aave.220410.nc -o gx1v7_nomarinland -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

```
./create_newcase --case replace_marinland --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi2
cd replace_marinland
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
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_nomarinland.220410.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_nomarinland.220410.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_nomarinland.220410.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_nomarinland.220410.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_nomarinland_aave.220410.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_nomarinland_blin.220410.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_nomarinland_patc.220410.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_nomarinland_TO_fv09_125_aave.220410.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_nomarinland_TO_fv09_125_aave.220410.nc'
```

# 更改海陆分布实验（四） 索马里地区

**制作domain文件**

```
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v7_220410_somali.nc -nocn gx1v7_somali --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1pt_nomarinland_TO_fv09_125_aave.220410.nc -o gx1v7_nomarinland -l fv09_125 -p 2
```

该实验在lym上跑

```
./create_newcase --case replace_somali --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd replace_somali
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
./xmlchange ATM_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv_09125_gx1v7_somali.220410.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv_09125_gx1v7_somali.220410.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_somali.220410.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_somali.220410.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_somali_aave.220410.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_somali_blin.220410.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_somali_patc.220410.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_somali_TO_fv09_125_aave.220410.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_somali_TO_fv09_125_aave.220410.nc'
```



# 更改海陆分布实验 （五） 去除印度大陆及中南半岛

**制作domain文件**

```shell
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v7_151008_noinch_noindian.nc -nocn gx1v7_noinch_noindian --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc -o gx1v7_noinch_noindian -l fv09_125 -p 2
cp *.nc /public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/
cd ../gen_mapping_files/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/gx1v7/
cp *nc ~/swh/cesm2.1.3/inputdata/cpl/gridmaps/fv0.9x1.25/
```

该实验在lym上跑

```shell
./create_newcase --case replace_inch_indian --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi2
cd replace_inch_indian
./xmlchange NTASKS=-20
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
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noinch_noindian.220420.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noinch_noindian.220420.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noinch_noindian.220420.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noinch_noindian.220420.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_aave.220420.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_blin.220420.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_patc.220420.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc'
```



# 更改海陆分布实验 （六） 去除印度大陆及海洋性大陆

**生成domain文件**

```
./gen_cesm_maps.sh --serial -fatm ~/swh/data/domain/fv0.9x1.25_141008.nc -natm fv09_125 -focn ~/swh/data/domain/gx1v7_151008_nosealand_noindian.nc -nocn gx1v7_nosealand_noindian --nogridcheck
./gen_domain -m ../gen_mapping_files/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc -o gx1v7_noinch_noindian -l fv09_125 -p 2
```

该实验在lym上跑

```
./create_newcase --case replace_sealand_indian --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd replace_sealand_indian
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_somali/user_nl_cam .
cp ../replace_somali/user_nl_docn .
cp ../replace_somali/user_nl_cice .
cp ../replace_somali/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_nosealand_noindian.220420.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_nosealand_noindian.220420.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_nosealand_noindian.220420.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_nosealand_noindian.220420.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_nosealand_noindian_aave.220420.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_nosealand_noindian_blin.220420.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_nosealand_noindian_patc.220420.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_nosealand_noindian_TO_fv09_125_aave.220420.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_nosealand_noindian_TO_fv09_125_aave.220420.nc'
```



# 海温实验



### f2000_test1

```
./create_newcase --case topo_indo_no_plateau --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd topo_indo_no_plateau
./xmlchange NTASKS=-24 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=24
./xmlchange RESUBMIT=2
./xmlchange REST_N=5
./xmlchange REST_OPTION=nmonths
./case.setup
```



### 测试能不能跑起来

```
./create_newcase --case f2000_test6 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_test6
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test1/user_nl_cam .
cp ../f2000_test1/sbatch1.sh .
```



### 测试能不能跑起来(更换更新的openmpi测试)

```
./create_newcase --case f2000_test8 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_test8
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test6/user_nl_cam .
cp ../f2000_test6/sbatch1.sh .

```

### 测试mpi3

```
./create_newcase --case f2000_test9 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_test9
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test6/user_nl_cam .
cp ../f2000_test6/sbatch1.sh .

不可行
```

### 测试服务器自带的module

```
./create_newcase --case f2000_test10 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_test10
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test6/user_nl_cam .
cp ../f2000_test6/sbatch1.sh .
```

### 程序报错 试试fhist能不能跑

```
./create_newcase --case fhist_test1 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd fhist_test1
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test6/user_nl_cam .
cp ../f2000_test6/sbatch1.sh .
```

FHIST是可以跑的，看来问题还是出在f2000的实验设置上，下一步检查inputdata是否有问题



# F2000 (一) 控制实验

```shell
./create_newcase --case f2000_control_220513 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_control_220513
./xmlchange NTASKS=-12 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp ../replace_somali/user_nl_cam .
cp ../replace_somali/sbatch1.sh .
```

# F2000（二）无印度大陆实验 lym服务器

```shell
./create_newcase --case change_indian_220515 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd change_indian_220515
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_sealand_indian/user_nl_cam .
cp ../replace_sealand_indian/user_nl_docn .
cp ../replace_sealand_indian/user_nl_cice .
cp ../replace_sealand_indian/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_swh.220401.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_swh.220401.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_aave.220401.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_blin.220401.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_swh_patc.220401.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_swh_TO_fv09_125_aave.220401.nc'
```



# F2000 (三) 无中南半岛实验 wgx服务器

```shell
./create_newcase --case f2000_replace_inch_220519 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_replace_inch_220519
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
./xmlchange ATM_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_noinch.220406.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1pt_noinch.220406.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_noinch.220406.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/wgx/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1pt_noinch.220406.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_aave.220406.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_blin.220406.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1pt_noinch_patc.220406.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_noinch_TO_fv09_125_aave.220406.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1pt_noinch_TO_fv09_125_aave.220406.nc'
```

# F2000(四)无中南半岛及印度大陆实验 lym服务器

```shell
./create_newcase --case f2000_replace_inch_indian2 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_replace_inch_indian2
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../f2000_replace_inch_indian/user_nl_cam .
cp ../f2000_replace_inch_indian/user_nl_docn .
cp ../f2000_replace_inch_indian/user_nl_cice .
cp ../f2000_replace_inch_indian/sbatch1.sh .
./xmlchange ATM_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noinch_noindian.220420.nc'
./xmlchange LND_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.lnd.fv09_125_gx1v7_noinch_noindian.220420.nc'
./xmlchange ICE_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noinch_noindian.220420.nc'
./xmlchange OCN_DOMAIN_FILE='/public1/home/lym/swh/cesm2.1.3/inputdata/share/domains/domain.ocn.gx1v7_noinch_noindian.220420.nc'
./xmlchange ATM2OCN_FMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_aave.220420.nc'
./xmlchange ATM2OCN_SMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_blin.220420.nc'
./xmlchange ATM2OCN_VMAPNAME='cpl/gridmaps/fv0.9x1.25/map_fv09_125_TO_gx1v7_noinch_noindian_patc.220420.nc'
./xmlchange OCN2ATM_FMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc'
./xmlchange OCN2ATM_SMAPNAME='cpl/gridmaps/gx1v7/map_gx1v7_noinch_noindian_TO_fv09_125_aave.220420.nc'
```





# F2000 (test on lym)

```
./create_newcase --case f2000_test_220514 --res f09_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd f2000_test_220514
./xmlchange NTASKS=-12 
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
```





# 高分辨率实验

**lym**

```
./create_newcase --case fhist_highres4 --res f05_g17 --compset F2000climo --run-unsupported --compiler intel --mach oneapi
cd fhist_highres4
./xmlchange NTASKS=-20
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 

```







# 耦合实验

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







# CESM使用过程中的bug

**在continue run的过程中，无法成功提交，我猜想是mpi的问题**

后续在中南半岛实验中试一下，使用相同的mpi再continue run

# 服务器使用过程中的记录

## 环境配置

1. 注意！！如果使用oneapi环境的话，首先是sun(alias，配置第一步环境)，然后oneapi(alias, 设置编译器)

   然后要source swh文件夹下的oneapi.sh 配置第二步环境才可以

## BUG

module服务器自带的mpi才好用，自己编译的mpi就算使用中模式编译成功了，也跑不起来



# 关于F2000运行中的输入问题

在我运行f2000的过程中报错，提示是输入文件的问题，文件名为

tracer_cnst_file = /public1/home/lym/swh/cesm2.1.3/inputdata/atm/cam/ozone/tracer_cnst_CAM6chem_2000climo_3D_monthly_c171004.nc

诡异的是ncdump还能出来结果，但是文件大小只有51m，后来在另一个服务器wgx上面比对发现那里面的是三百多兆，把文件拿过来用就能正常运行了







## 配置刘老师服务器

跑模式测试

```
./create_newcase --case lym_test3 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd lym_test3
./xmlchange NTASKS=-8 
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=5
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nmonths
./case.setup
cp ../f2000_test6/user_nl_cam .
cp ../f2000_test6/sbatch1.sh .
```

这里总结一下登录刘老师服务器后的设置

登陆之后 'sun',然后读取source文件就可以了





# CESM2实验日志

## F2000系列实验

<font color='red'>之前跑的FHIST实验我认为可能引入了无关变量，这里跑一组F2000的实验</font>

### 控制实验

```
平台 wgx 
时间 2022-5-13 
案例名 f2000_control_220513
已同步至本地

问题记录：由于内存空间不够发现已断开，已提交重新跑(20)
```

### 无印度大陆实验

```
平台 lym
时间 2022-5-15 
案例名 change_indian_220515

```

### 无中南半岛实验

```
平台 wgx
时间 2022-5-19
案例名 f2000_replace_inch
```

## 无中南半岛及印度大陆实验

```
平台 lym
时间 2022-5-20
案例名 f2000_replace_inch_indian2
```





# 网上资源

[(58条消息) CESM2 实验笔记_一株草的世界的博客-CSDN博客](https://blog.csdn.net/qq_38607066/article/details/109445839?spm=1001.2014.3001.5502)



## Controlling starting, stopping and restarting a run

The case initialization type is set in `env_run.xml`. A CESM run can be initialized in one of three ways; startup, branch, or hybrid.



- startup

  In a startup run (the default), all components are initialized using baseline states. These baseline states are set independently by each component and can include the use of restart files, initial files, external observed data files, or internal initialization (i.e., a "cold start"). In a startup run, the coupler sends the start date to the components at initialization. In addition, the coupler does not need an input data file. In a startup initialization, the ocean model does not start until the second ocean coupling (normally the second day).

- branch

  In a branch run, all components are initialized using a consistent set of restart files from a previous run (determined by the $`RUN_REFCASE` and $`RUN_REFDATE` variables in `env_run.xml`). The case name is generally changed for a branch run, although it does onot have to be. In a branch run, setting $`RUN_STARTDATE` is ignored because the model components obtain the start date from their restart datasets. Therefore, the start date cannot be changed for a branch run. This is the same mechanism that is used for performing a restart run (where $`CONTINUE_RUN` is set to TRUE in the `env_run.xml` file).Branch runs are typically used when sensitivity or parameter studies are required, or when settings for history file output streams need to be modified while still maintaining bit-for-bit reproducibility. Under this scenario, the new case is able to produce an exact bit-for-bit restart in the same manner as a continuation run *if* no source code or component namelist inputs are modified. All models use restart files to perform this type of run. $`RUN_REFCASE` and $`RUN_REFDATE` are required for branch runs.To set up a branch run, locate the restart tar file or restart directory for $`RUN_REFCASE` and $`RUN_REFDATE` from a previous run, then place those files in the $`RUNDIR` directory. See [setting up a branch run](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/usersguide/x2012.html) for an example.

- hybrid

  A hybrid run indicates that CESM is initialized more like a startup, but uses initialization datasets *from a previous case*. This is somewhat analogous to a branch run with relaxed restart constraints. A hybrid run allows users to bring together combinations of initial/restart files from a previous case (specified by $`RUN_REFCASE`) at a given model output date (specified by $`RUN_REFDATE`). Unlike a branch run, the starting date of a hybrid run (specified by $`RUN_STARTDATE`) can be modified relative to the reference case. In a hybrid run, the model does not continue in a bit-for-bit fashion with respect to the reference case. The resulting climate, however, should be continuous provided that no model source code or namelists are changed in the hybrid run. In a hybrid initialization, the ocean model does not start until the second ocean coupling (normally the second day), and the coupler does a "cold start" without a restart file.

The variable `$RUN_TYPE` determines the initialization type. This setting is only important for the initial run of a production run when the `$CONTINUE_RUN` variable is set to FALSE. After the initial run, the `$CONTINUE_RUN` variable is set to TRUE, and the model restarts exactly using input files in a case, date, and bit-for-bit continuous fashion. The variable `$RUN_TYPE` is the start date (in yyyy-mm-dd format) either a startup or hybrid run. If the run is targeted to be a hybrid or branch run, you must also specify values for `$RUN_REFCASE` and `$RUN_REFDATE`. All run startup variables are discussed in [run start control variables](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/modelnl/env_run.html#run_start).

Before a job is submitted to the batch system, you need to first check that the batch submission lines in `$CASE.run` are appropriate. These lines should be checked and modified accordingly for appropriate account numbers, time limits, and stdout/stderr file names. You should then modify `env_run.xml` to determine the key run-time settings. See [controlling run termination](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/modelnl/env_run.html#run_stop), [controlling run restarts](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/modelnl/env_run.html#run_rest), and [performing model restarts ](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/usersguide/x1594.html#running_ccsm_restarts)for more details. A brief note on restarting runs. When you first begin a branch, hybrid or startup run, CONTINUE_RUN must be set to FALSE. When you successfully run and get a restart file, you will need to change CONTINUE_RUN to TRUE for the remainder of your run. See [performing model restarts ](https://www.cesm.ucar.edu/models/cesm1.1/cesm/doc/usersguide/x1594.html#running_ccsm_restarts)for more details.

By default,

```
STOP_OPTION = ndays STOP_N = 5 STOP_DATE = -999 
```



The default setting is only appropriate for initial testing. Before a longer run is started, update the stop times based on the case throughput and batch queue limits. For example, if the model runs 5 model years/day, set `RESUBMIT`=30, `STOP_OPTION`= nyears, and `STOP_N`= 5. The model will then run in five year increments, and stop after 30 submissions.

