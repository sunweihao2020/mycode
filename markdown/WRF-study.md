---
title: WRF-study
date: 2022-06-24 15:16:47
tags:
---



> The WRF system contains two dynamical solvers, referred to as the ARW (Advanced Research WRF) core and the NMM (Nonhydrostatic Mesoscale Model) core. The ARW has been developed in large part and is maintained by NCAR's Mesoscale and Microscale Meteorology Laboratory, and its users' page is: [WRF-ARW Users' Page](http://www.mmm.ucar.edu/wrf/users/). The NMM core was developed by the National Centers for Environmental Prediction (NCEP), and is currently used in their HWRF (Hurricane WRF) system.

# WRF

## 安装

参考：

[Compiling WRF (ucar.edu)](https://www2.mmm.ucar.edu/wrf/OnLineTutorial/compilation_tutorial.php)

# 安装记录

```shell
export DIR=/home/sun/build_wrf/libraries
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS="-m64"
export F77=gfortran
export FFLAGS="-m64"
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include
export LDFLAGS="-L$DIR/grib2/lib"
export CPPFLAGS="-I$DIR/grib2/include"


export PATH=$DIR/netcdf/bin:$PATH
export NETCDF=$DIR/netcdf
```

在安装WRF ./configure这一步会报错，有个warning

根据提示输入

```shell
export NETCDF_classic=1
```

重新./configure即可，但是报错了，显示编译器测试不通过。可是官网提供的例子我测试都是通过了的。也许我应该换个低版本的编译器再试试<font color=red>(220711)</font>



### 安装220711记录

使用github上的安装sh脚本成功安装，该库已fork，安装位置在

/home/sun/Build_WRF

```shell
export DIR=/home/sun/app/gcc9.5_library
export CC=gcc
export CXX=g++
export FC=gfortran
export FCFLAGS="-m64"
export F77=gfortran
export FFLAGS="-m64"
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include
export LDFLAGS="-L$DIR/grib2/lib"
export CPPFLAGS="-I$DIR/grib2/include"


export PATH=$DIR/netcdf/bin:$PATH
export NETCDF=$DIR/netcdf
export PATH=$DIR/mpich/bin:$PATH
```

上面使用gcc9.5来运行也会报错，报错信息

```
Error Error Error NoahMP submodule files not populating WRF directories
```



```shell
export DIR=/home/sun/app/oneapi_library
export CC=icc
export CXX=icpc
export FC=ifort
export FCFLAGS="-m64"
export F77=ifort
export FFLAGS="-m64"
export JASPERLIB=$DIR/grib2/lib
export JASPERINC=$DIR/grib2/include
export LDFLAGS="-L$DIR/grib2/lib"
export CPPFLAGS="-I$DIR/grib2/include"


export PATH=$DIR/netcdf/bin:$PATH
export NETCDF=$DIR/netcdf
export PATH=$DIR/mpich/bin:$PATH
```

<font color=red>依然报错，但是官网给的测试例子是通过了，目前通过github上的脚本安装成功，但是我怀疑这可能是跟ubuntu22.04有关，脚本作者也说到新版本装wrf可能会出问题。以及过去在旧的版本ubuntu上是可以安装成功的</font>



# MPAS学习



## 资料

[UFS Weather Model Users Guide (ufs-weather-model.readthedocs.io)](https://ufs-weather-model.readthedocs.io/_/downloads/en/latest/pdf/) 文档





## 安装

1. 在lym上安装所需要的库 p-cetcdf PIO

```shell
export CC=icc
export FC=ifort
export F77=ifort
export MPICC=mpiicc
export MPIF90=mpiifort
export MPIF77=mpiifort
export PNETCDF=/public1/home/lym/swh/app/intel/netcdf4

```

```shell
export MPIFC=mpiifort
export PNETCDF_PATH=$PNETCDF
export PIO=/public1/home/lym/swh/app/intel/netcdf
./configure --prefix=$PIO --disable-netcdf --disable-mpiio
```

在安装mpas的过程中报错，现在通过gcc的编译器来安装一遍试试

1. <font color=red>mpich3.3.1版本就可以，其他版本会报错，不知道原因</font>

2. netcdf-fortran安装失败



2022-6-25进度：失败了，装不上，不装了

2022-7-1进度

![image-20220701150653440](C:\Users\nuist\AppData\Roaming\Typora\typora-user-images\image-20220701150653440.png)

好像成功了？回头看看



## 2022-7-10安装记录

netcdf-fortran没能安装成功orz



d-30 d-20 d-10 slide 重画

slide 7 
