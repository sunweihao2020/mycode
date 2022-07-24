---
title: oneapi在移植CESM2中的应用
date: 2022-04-15 15:02:56
tags: CESM
comment: 'valine'
categories: model
---

**OneAPI 在 CESM2 移植中的应用**



Intel 最近几年发布了oneapi，简单说来就是把编译器、MPI库、数学计算库等等软件都放在一个工具包中，使用起来十分的方便不需要再像之前那样装些乱七八糟的软件了。它官网自己都说了，**say goodbye to proprietary Lock-In**

<img src="https://z4a.net/images/2022/04/15/-2022-04-15-151743.png" alt="-2022-04-15-151743.png" style="zoom: 50%;" />

更重要的是——免费！这里点赞Intel

<font size=5>本文记录一下我使用oneapi工具包将CESM2移植到服务器上的流程</font>



# 关于oneapi的安装

首先是oneapi的官网：

https://www.intel.com/content/www/us/en/developer/tools/oneapi/overview.html#gs.ww0qvh

[![1c13582f6f20b44ae.md.png](https://z4a.net/images/2022/04/15/1c13582f6f20b44ae.md.png)](https://z4a.net/image/2OQuAp)



点击红色箭头所指处进入工具包列表，红色框中所框出来的两个就是我们需要用到的安装包，分别安装两个工具包的流程都是一样的，这里仅以第二个HPC toolkit为例，注意这里建议先安装框中下面那个：

[![22cf048aaae7b1186.md.png](https://z4a.net/images/2022/04/15/22cf048aaae7b1186.md.png)](https://z4a.net/image/2OQEsJ)



## 安装HPC Toolkit

点击上图所示的链接后，在跳出来的软件列表里选择HPC Toolkit那一栏下方有个Download，点击。在选项中依次选择图中的几个选项，最后一个选择offline

![-2022-04-15-152920.png](https://z4a.net/images/2022/04/15/-2022-04-15-152920.png)



选择完后旁边会跳出来下载链接，点击下载就好了。



下载完成后把该文件上传到服务器，这个文件本身是一个sh文件，所以

```
sh 文件名.sh
```

加载一段时间后会跳出来安装界面，可以选择全部安装or自定义安装，省事的话一直点下一步就可以了。安装完成后会自动退出。

以上是HPC Toolkit的安装过程，另一个安装包Base toolkit安装流程是一样的。<font color=#FF000>这里再次建议先安装HPC Toolkit再安装Base Toolkit</font>



在这个两个包安装完成后，很多我们需要的软件就已经在我们服务器中了，但是我们由于没有把他们加到环境变量中系统是不知道我们安装的软件在哪里的。这里intel贴心地给我们生成了一个sh文件，source一下就把各种软件加进环境变量了。

该文件位置以及环境配置大致如下：

```shell
source $HOME_PATH/intel/oneapi/setvars.sh
```

结果如图，意思就是环境都给你配置好了 此时可以输入 "icc -v"查看一下

[![-2022-04-15-153836.png](https://z4a.net/images/2022/04/15/-2022-04-15-153836.png)](https://z4a.net/image/2OQMfj)



<font size=5>下面小结一下我们安装了这两个包里分别都包含那些我们需要的软件</font>

HPC Toolkit： 编译器（icc icpc ifort） 并行计算库（intelmpi）

Base Toolkit:  MKL数学库（BLAS和LAPACK)



# python的安装

CESM2的编译安装是需要python3版本以上的，服务器默认的往往是python2，所以需要自己进行安装，这里我图省事直接用安装了conda然后创建了一个环境，关于conda和conda创建环境网上资料非常多，也很简单，这里不再赘述。

提个我认为需要注意的点：

1. 建议安装miniconda，是conda精简版，占用地方小。miniconda下载网址[Miniconda — Conda documentation](https://docs.conda.io/en/latest/miniconda.html) 选python3.7的linux版本进行下载就好，版本不需要太高。下载完上传到服务器里sh一下就自动安装了。



# netcdf库的安装

上述过程完成后，最后一个重要的准备工作就是安装netcdf库了，这里有些人还安装了pnetcdf库，是一个并行的的netcdf库但是我尝试没有成功，不装pnetcdf也是可以的。这里只介绍netcdf库安装。注意在这之前前两步都做完了以及把编译器的环境变量都给配置好。

```shell
icc -v
```

查看一下编译器是否加入环境路径

参考链接：

[关于clm5.0移植的过程记录（初学者） - 知乎 (zhihu.com)](https://zhuanlan.zhihu.com/p/183752623)

安装步骤：

1. 安装zlib库

   下载地址 http://www.zlib.net/zlib-1.2.11.tar.gz

   ```shell
   wget http://www.zlib.net/zlib-1.2.11.tar.gz
   tar -zxvf ./zlib-1.2.11.tar.gz
   cd zlib-1.2.11.tar.gz
   export CC=icc
   export CXX=icpc
   export FC=ifort
   export f77=ifort
   ./configure --prefix=/public1/home/lym/swh/app/intel/netcdf4
   make
   make install
   ```

   这里面export作用是把编译过程中的默认选项切换到intel的编译器，./configure --prefix选项的作用是指定你编译安装的路径，这里可根据自己喜好更改。

2. 安装curl

   这个软件服务器自带的，所以我没有安装，可以查看下服务器上是都有这个软件：

   ```shell
   curl --version
   ```

3. 安装hdf5

   下载官网：https://www.hdfgroup.org/downloads/hdf5/source-code/

   ```shell
   tar -zxvf ./hdf5-1.12.0.tar.gz
   cd hdf5-1.12.0
   export CC=icc
   export CXX=icpc
   export FC=ifort
   export f77=ifort
   CFLAGS="-O3 -fPIC" CPPFLAGS="-O3 -fPIC" FFLAGS="-O3 -fPIC" FFLAGS="-O3 -fPIC" LIBS="-ldl"
   ./configure --prefix=/public1/home/lym/swh/app/intel/netcdf4 --with-zlib=/public1/home/lym/swh/app/intel/netcdf4 --enable-largefile --enable-static --enable-shared --enable-fortran --enable-hl
   make && make install
   ```

   这里如果你没有重新登陆的话，四个export其实已经不需要了

4. 安装netcdf库

   下载：

   ```shell
   wget ftp://ftp.unidata.ucar.edu/pub/netcdf/netcdf-4.6.1.tar.gz
   ```

   安装

   ```shell
   tar -zxvf ./netcdf-4.6.1.tar.gz
   cd netcdf-4.6.1
   export CC=icc
   export CXX=icpc
   export FC=ifort
   export f77=ifort
   CFLAGS="-O3 -fPIC -I/public1/home/lym/swh/app/intel/netcdf4/include" CPPFLAGS="-O3 -fPIC -I/public1/home/lym/swh/app/intel/netcdf4/include" FFLAGS="-O3 -fPIC" LDFLAGS=-L/public1/home/lym/swh/app/intel/netcdf4/lib ./configure --prefix=/public1/home/lym/swh/app/intel/netcdf4 --enable-static --enable-shared --enable-netcdf4 --enable-largefile --enable-large-file-tests --enable-diskless --enable-mmap --with-zlib=/public1/home/lym/swh/app/intel/netcdf4
   make
   make install
   ```

   注意上述操作中出现的路径仅供参考，实际情况是要根据你在前几步安装过程进行调整。安装成功后会蹦出来个欢迎界面，开头是congratulations，表示你成功了。

5. 安装netcdf-c库

   下载：

   ```shell
   wget https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-c-4.7.0.tar.gz	
   ```

   安装

   ```shell
   tar -zxvf ./netcdf-c-4.7.0.tar.gz
   cd netcdf-c-4.7.0
   export CC=icc
   export CXX=icpc
   export FC=ifort
   export f77=ifort
   CPPFLAGS=-I/public1/home/lym/swh/app/intel/netcdf4/include LDFLAGS=-L/public1/home/lym/swh/app/intel/netcdf4/lib ./configure --prefix=/public1/home/lym/swh/app/intel/netcdf4
   ```

6. 安装netcdf-fortran库

   下载：

   ```shell
   wget https://www.unidata.ucar.edu/downloads/netcdf/ftp/netcdf-fortran-4.4.5.tar.gz
   ```

   安装

   ```shell
   tar -xvf ./netcdf-fortran-4.4.5.tar.gz
   cd netcdf-fortran-4.4.5
   export LD_LIBRARY_PATH=/public1/home/lym/swh/app/intel/netcdf4/lib:$LD_LIBRARY_PATH
   export CC=icc
   export CXX=icpc
   export FC=ifort
   export f77=ifort
   CFLAGS="-O3 -fPIC -I/public1/home/lym/swh/app/intel/netcdf4/include" FFLAGS="-O3 -fPIC" FCFLAGS="-O3 -fPIC" LDFLAGS=-L/public1/home/lym/swh/app/intel/netcdf4/lib LIBS="-lnetcdf -lhdf5_hl -lhdf5 -lz -lm -ldl" ./configure --prefix=/public1/home/lym/swh/app/intel/netcdf4 --enable-static --enable-shared --enable-logging --enable-largefile --enable-large-file-tests --with-zlib=/public1/home/lym/swh/app/intel/netcdf4
   make && make install
   ```



**至此，netcdf库基本算安装完成**

将netcdf库加入环境变量，自己做一个sh文件，在其中对netcdf的环境变量进行设置，然后登录上服务器后source下该文件即可

我的设置如图：

![-2022-04-15-162254.png](https://z4a.net/images/2022/04/15/-2022-04-15-162254.png)

source完检查一下是否加入到环境变量，以及查看上述软件是否都被正确安装，使用命令：

```shell
nc-config --all
```

[![-2022-04-15-162527.md.png](https://z4a.net/images/2022/04/15/-2022-04-15-162527.md.png)](https://z4a.net/image/2OQbwE)



# BLAS与LAPACK的安装

BLAS与LAPACK是两个数学计算库，CESM运行需要用到它们，前面安装oneapi的的时候实际已经安装上他们俩，在mkl库里面。但是在应用的过程中我发现在编译CESM2的过程中调用LAPACK库的时候会出现bug，最后还是重新安装了。这里只安装LAPACK库，BLAS不用安装，后续直接调用oneapi里面的库即可。

安装过程参考[linux下安装blas和lapack_baiyang3的博客-CSDN博客_linux 安装lapack](https://blog.csdn.net/baiyang3/article/details/52790793)

## 下载lapack后解压

```shell
tar -zxvf lapack-3.10.0.tgz
cd lapack-3.10.0/INSTALL/
```

然后根据平台的特点，将INSTALL目录下对应的make.inc.XXX复制一份到 lapack-3.10.0目录下，并命名为make.inc, 这里我复制的是INSTALL/make.inc.ifot，因为我这里用的是intel编译器。

```shell
cp make.inc.ifort ../make.inc
cd ..
make
```

这里要注意版本问题，lapack好像从3.5版本之后不需要先安装blas再拷贝一些库进去了，直接在lapack目录里make就行，所以这里建议使用新版本的lapack，亲测使用3.4.2版本会报错。

make完成之后：

```shell
cd LAPACKE
make
```

编译不报错的话，LAPACK库到此就完成了，记住该目录的路径，后面移植的时候要用



# CESM2.1.3的移植

以上是几个比较关键的库，除此之外还需要SVN git等等工具，一般服务器都自带，不自带的话安装也比较简单网上很多教程。这里就不展开了，接下来说CESM2的移植。此处版本为cesm2.1.3

# 源代码的下载

官网教程

[Downloading CESM2 (CESM2.1) — CESM CESM2.1 documentation (escomp.github.io)](https://escomp.github.io/CESM/versions/cesm2.1/html/downloading_cesm.html)

在这一步：

```shell
./manage_externals/checkout_externals
```

执行后会自动开始下载CESM2所需要的各个模块的组件，但是由于一些众所周知的原因，我们不能畅通地连接外网，为解决这个问题可以使用下载完组件后打包安装的压缩包，解压到自己目录即可。

这里提供百度云链接，版本为cesm2.1.3

链接：https://pan.baidu.com/s/1GBghBIaF-8bey-ND7aK5gQ 
提取码：m7m7

解压好后可以

```shell
./manage_externals/checkout_externals -S
```

检查一下各个组件有无问题，如果没有问题结果应该是这样的：

[![-2022-05-12-105643.md.png](https://z4a.net/images/2022/05/12/-2022-05-12-105643.md.png)](https://z4a.net/image/2mj3WH)



# config的设置

装好CESM2.1.3之后，接下来就要处理移植的配置文件

首先是在home目录下建立一个.cime目录

```shell
mkdir ~/.cime
```

这个目录下面将要包含三个文件：

config_batch.xml           **该文件包含提交到节点运算方面的一些配置**

config_compilers.xml   **该文件包含编译器、mpi库、以及其他一些库的配置**

config_machines.xml   **该文件包含一些路径等等的配置**



<font face="微软雅黑">这三个文件官方是有提供模板的，位置在$HOME/cesm2.1.3/cime/config/cesm/machines 下面，打开xml的文件话会看到里面已经提供了多套配置，以config_compilers.xml为例，用**gcc** or **intel compiler** or **PGI**的话,不同的编译器官网给你提供了现成的模板，选择你需要的那套，其余的就都可以删了，这里建议先把上述三个文件拷贝到~/.cime目录下然后进行修改</font>

<font color='red'>下面我贴出自己的config文件，并对我认为重要的地方进行标注，仅供参考根据自己平台和编译器的不同要自己做修改</font>

<font size=12>config_machines</font>

```xml
<?xml version="1.0"?>

<config_machines version="2.0">
<machine MACH="oneapi2">
  <DESC>sunweihao</DESC>                                 
  <NODENAME_REGEX>login01</NODENAME_REGEX>
  <OS>LINUX</OS>
  <PROXY>sunweihao</PROXY>
  <COMPILERS>intel</COMPILERS>      # 标出所使用的编译器，这里用的是intel
  <MPILIBS>intelmpi</MPILIBS>       # 标出所使用的mpi，这里用的intelmpi
  <PROJECT>none</PROJECT>
  <CIME_OUTPUT_ROOT>/public1/home/wgx/swh/cesm2.1.3/scratch</CIME_OUTPUT_ROOT>  # 这个路径是跑case时的运行路径
  <DIN_LOC_ROOT>/public1/home/wgx/swh/cesm2.1.3/inputdata</DIN_LOC_ROOT>
  <DIN_LOC_ROOT_CLMFORC>/public1/home/wgx/swh/cesm2.1.3/inputdata/atm/datm7</DIN_LOC_ROOT_CLMFORC>
  <DOUT_S_ROOT>/public1/home/wgx/swh/cesm2.1.3/archive/$CASE</DOUT_S_ROOT>
  <BASELINE_ROOT>/public1/home/wgx/swh/cesm2.1.3/cesm_baselines</BASELINE_ROOT>
  <CCSM_CPRNC>/public1/home/wgx/swh/cesm2.1.3/cime/tools/cprnc</CCSM_CPRNC>
  <GMAKE>make</GMAKE> 
  <GMAKE_J>24</GMAKE_J>               # make时所使用的核数
  <BATCH_SYSTEM>slurm</BATCH_SYSTEM>  # 这里要给出你所在服务器上使用的作业管理系统
  <SUPPORTED_BY>swh</SUPPORTED_BY>
  <MAX_TASKS_PER_NODE>28</MAX_TASKS_PER_NODE>    # 这里是每个结点的最大核数，会因为服务器不同而不同，要事先查好
  <MAX_MPITASKS_PER_NODE>28</MAX_MPITASKS_PER_NODE>
  <PROJECT_REQUIRED>FALSE</PROJECT_REQUIRED>
  <mpirun mpilib="default">
    <executable>mpirun</executable>
    <arguments>
<arg name="ntasks"> -np {{ total_tasks }} </arg>
    </arguments>
  </mpirun>
  <module_system type="none">
  </module_system>
  <environment_variables>       #前面安装的一些软件库的路径
    <env name="OMP_STACKSIZE">256M</env>
    <env name="PATH">$ENV{HOME}/bin:$ENV{PATH}</env>
    <env name="NETCDF_PATH">/public1/home/wgx/swh/app/oneapi/netcdf4</env>
    <env name="HDF5_PATH">/public1/home/wgx/swh/app/oneapi/netcdf4</env>
    <env name="ZLIB_PATH">/public1/home/wgx/swh/app/oneapi/netcdf4</env>
    <env name="LAPACK_PATH">/public1/home/wgx/intel/oneapi/mkl/2021.3.0</env>
  </environment_variables>
  <resource_limits>
    <resource name="RLIMIT_STACK">-1</resource>
  </resource_limits>
</machine>
</config_machines>
```



<font size=12>config_compliers</font>

```xml
<?xml version="1.0" encoding="UTF-8"?>
<config_compilers version="2.0">
<compiler COMPILER="intel" MACH="oneapi2"> # 这里给出使用intel编译器的时候的配置
  <CFLAGS>
    <base>  -qno-opt-dynamic-align -fp-model precise -std=gnu99 </base>
    <append compile_threaded="true"> -qopenmp </append>
    <append DEBUG="FALSE"> -O2 -debug minimal </append>
    <append DEBUG="TRUE"> -O0 -g </append>
  </CFLAGS>
  <CPPDEFS>
    <!-- http://software.intel.com/en-us/articles/intel-composer-xe/ -->
    <append> -DFORTRANUNDERSCORE -DCPRINTEL</append>
  </CPPDEFS>
  <CXX_LDFLAGS>
    <base> -cxxlib </base>
  </CXX_LDFLAGS>
  <CXX_LINKER>FORTRAN</CXX_LINKER>
  <FC_AUTO_R8>
    <base> -r8 </base>
  </FC_AUTO_R8>
  <FFLAGS>
    <base> -qno-opt-dynamic-align  -convert big_endian -assume byterecl -ftz -traceback -assume realloc_lhs -fp-model source  </base>
    <append compile_threaded="true"> -qopenmp </append>
    <append DEBUG="TRUE"> -O0 -g -check uninit -check bounds -check pointers -fpe0 -check noarg_temp_created </append>
    <append DEBUG="FALSE"> -O2 -debug minimal </append>
  </FFLAGS>
  <FFLAGS_NOOPT>
    <base> -O0 </base>
    <append compile_threaded="true"> -qopenmp </append>
  </FFLAGS_NOOPT>
  <FIXEDFLAGS>
    <base> -fixed -132 </base>
  </FIXEDFLAGS>
  <FREEFLAGS>
    <base> -free </base>
  </FREEFLAGS>
  <LDFLAGS>
    <append compile_threaded="true"> -qopenmp </append>
  </LDFLAGS>
  <MPICC> mpiicc  </MPICC>
  <MPICXX> mpicpc </MPICXX>
  <MPIFC> mpiifort </MPIFC>
  <SCC> icc </SCC>
  <SCXX> icpc </SCXX>
  <SFC> ifort </SFC>
  <MPI_PATH>/public1/home/wgx/intel/oneapi/mpi/2021.5.1</MPI_PATH>  # 此处路径要对应oneapi里面mpi库的路径
  <SLIBS>
    <append> -L/public1/home/wgx/swh/app/oneapi/netcdf4/lib -lnetcdff -lnetcdf </append> # 标出netcdf库路径，跟上面软件安装路径一致
    <append> -L/public1/home/wgx/intel/oneapi/mkl/2021.3.0 -lblas -L/public1/home/wgx/swh/app/oneapi/lapack-3.10.0 -llapack </append>            # blas和lapace的路径，blas只需要找到oneapi的里面mkl库路径即可，lapack前面我们有安装，这里是安装之后的路径
  </SLIBS>
  <SUPPORTS_CXX>TRUE</SUPPORTS_CXX>
</compiler>
</config_compilers>
```

<font size=12>config_batch</font>

```xml
<?xml version="1.0"?>
<config_batch version="2.1">
<batch_system type="slurm" MACH="oneapi2">
  <batch_submit>sbatch</batch_submit>
  <submit_args>
    <arg flag="--time" name="$JOB_WALLCLOCK_TIME"/>
    <arg flag="-p" name="$JOB_QUEUE"/>
  </submit_args>
  <queues>
    <queue walltimemax="12:00:00" nodemin="1" nodemax="2712">i01203share</queue> #i01203share是服务器能提交作业的队列名
  </queues>                                        # walltimemax时作业的时间最大限制，注意有些服务器是限制作业时长的
</batch_system>                                    # 这个时候我们就需要限制单次最大时长，然后多次提交

</config_batch>
```

以上三个文件设置好之后就可以去测试移植成果了~

