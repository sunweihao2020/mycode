---
title: CESM2-branch
date: 2022-06-03 18:13:26
tags: CESM
categories: model
---

# 一个关于branch实验的记录

## 基础实验

```shell
./create_newcase --case base_branch --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd base_branch
./xmlchange NTASKS=-8
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=2
./xmlchange RESUBMIT=2
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/sbatch1.sh .
```

```shell
./create_newcase --case base_branch2 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd base_branch2
./xmlchange NTASKS=-8
./xmlchange STOP_OPTION=nmonths
./xmlchange STOP_N=2
./xmlchange RESUBMIT=2
./xmlchange REST_N=1
./xmlchange REST_OPTION=nmonths
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/sbatch1.sh .
```

base2被我弄坏了，重新试

```
./create_newcase --case base_branch3 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd base_branch3
./xmlchange NTASKS=-8
./xmlchange STOP_OPTION=ndays
./xmlchange STOP_N=1
./xmlchange RESUBMIT=10
./xmlchange REST_N=1
./xmlchange REST_OPTION=ndays
./case.setup 
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/sbatch1.sh .
```



## branch测试

<font size=5.5>试试不修改其他的量能编译跑起来吗？</font>

```shell
./create_newcase --case test_branch3 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd test_branch3
./xmlchange RUN_REFCASE=base_branch3
./xmlchange RUN_REFDATE=0001-01-03
./xmlchange RUN_TYPE=branch
./case.setup
./case.build
```

没跑成功，查看log显示：

[![-2022-06-03-215629.png](https://z4a.net/images/2022/06/03/-2022-06-03-215629.png)](https://z4a.net/image/2EJ8FN)

这次修改一下核数再试试

```shell
./create_newcase --case test_branch4 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd test_branch4
./xmlchange NTASKS=-8
./xmlchange RUN_REFCASE=base_branch3
./xmlchange RUN_REFDATE=0001-01-03
./xmlchange RUN_TYPE=branch
./case.setup
cp ../replace_india8/user_nl_cam .
cp ../replace_india8/sbatch1.sh .
./case.build
```

<font color=red>我猜应该是refdate设置错了</font>

```
./create_newcase --case test_branch5 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd test_branch5
./xmlchange NTASKS=-8
./xmlchange RUN_REFCASE=base_branch3
./xmlchange RUN_REFDATE=1979-01-03
./xmlchange RUN_TYPE=branch
./case.setup
cp ../replace_india8/user_nl_cam .
cp ../test_branch4/sbatch1.sh .
./case.build
```

搞坏了。。

```
./create_newcase --case test_branch6 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd test_branch6
./xmlchange NTASKS=-8
./xmlchange RUN_REFCASE=base_branch3
./xmlchange RUN_REFDATE=1979-01-03
./xmlchange RUN_TYPE=branch
./case.setup
cp ../replace_india8/user_nl_cam .
cp ../test_branch4/sbatch1.sh .
./case.build
```



# 耦合实验的branch测试

```shell
./create_newcase --case b1850_tx4_indian_220618 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx4_indian_220618
./xmlchange NTASKS=-50
./xmlchange RUN_REFCASE=b1850_tx4_indian_220616
./xmlchange RUN_REFDATE=0011-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=3
./xmlchange RESUBMIT=60
./xmlchange REST_N=3
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_cice .
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

cp b1850_tx4_indian_220616/run/*.r.* b1850_tx4_indian_220618/run/
cp b1850_tx4_indian_220616/run/*.rs.* b1850_tx4_indian_220618/run/
cp b1850_tx4_indian_220616/run/*rpo* b1850_tx4_indian_220618/run/
```

## 中途修改了PHIS的branch测试

```
./create_newcase --case b1850_tx5_indian_220621 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx5_indian_220621
./xmlchange NTASKS=-30
./xmlchange RUN_REFCASE=b1850_tx4_indian_220618
./xmlchange RUN_REFDATE=0038-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=20
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx4_indian_220616/user_nl_cice .
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

cp b1850_tx4_indian_220616/run/*.r.* b1850_tx4_indian_220618/run/
cp b1850_tx4_indian_220616/run/*.rs.* b1850_tx4_indian_220618/run/
cp b1850_tx4_indian_220616/run/*rpo* b1850_tx4_indian_220618/run/
```



```
./create_newcase --case b1850_tx6_indian_220622 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx6_indian_220622
./xmlchange NTASKS=-50
./xmlchange RUN_REFCASE=b1850_tx5_indian_220621
./xmlchange RUN_REFDATE=0040-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=3
./xmlchange RESUBMIT=55
./xmlchange REST_N=3
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cice .
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

```
./create_newcase --case b1850_control4_220624 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_control4_220624
./xmlchange NTASKS=-30
./xmlchange RUN_REFCASE=b1850m_control3_220617
./xmlchange RUN_REFDATE=0053-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=55
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850m_control3_220617/sbatch1.sh .
./case.build --skip-provenance-check

cp b1850m_control3_220617/run/*.r.* b1850_control4_220624/run/
cp b1850m_control3_220617/run/*.rs.* b1850_control4_220624/run/
cp b1850m_control3_220617/run/*rpo* b1850_control4_220624/run/
```



# hybrid

```shell
./create_newcase --case b1850_tx_indian_220627 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_indian_220627
./xmlchange NTASKS=-40
./xmlchange RUN_REFCASE=b1850_tx6_indian_220622
./xmlchange RUN_REFDATE=0061-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx5_indian_220621/user_nl_cice .
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

cp b1850_tx6_indian_220622/run/*.r.* b1850_tx_indian_220627/run/
cp b1850_tx6_indian_220622/run/*.rs.* b1850_tx_indian_220627/run/
cp b1850_tx6_indian_220622/run/*rpo* b1850_tx_indian_220627/run/
cp b1850_tx6_indian_220622/run/*.i.* b1850_tx_indian_220627/run/
```

## （二）海洋性大陆实验重启

```shell
./create_newcase --case b1850_tx_maritime_h1_220629 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_maritime_h1_220629
./xmlchange NTASKS=-40
./xmlchange RUN_REFCASE=b1850_tx4_maritime_220624
./xmlchange RUN_REFDATE=0027-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=50
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx4_maritime_220624/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx4_maritime_220624/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx4_maritime_220624/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx4_maritime_220624/user_nl_cice .
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

cp b1850_tx4_maritime_220624/run/*.r.* b1850_tx_maritime_h1_220629/run/
cp b1850_tx4_maritime_220624/run/*.rs.* b1850_tx_maritime_h1_220629/run/
cp b1850_tx4_maritime_220624/run/*rpo* b1850_tx_maritime_h1_220629/run/
cp b1850_tx4_maritime_220624/run/*.i.* b1850_tx_maritime_h1_220629/run/
```

海洋性大陆实验重启h1 由于wgx服务器满了，这里转移到lym服务器上运行,由于是继续运行branch，所以依然命名为h1
```shell
./create_newcase --case b1850_tx_maritime_h1_220721 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_maritime_h1_220721
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_tx_maritime_h1_220629
./xmlchange RUN_REFDATE=0041-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=30
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx_maritime_h1_220629/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx_maritime_h1_220629/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx_maritime_h1_220629/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_tx_maritime_h1_220629/user_nl_cice .
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

海洋性大陆重启h2 lym服务器上运行，这里不知道为什么到第60年左右运行不了了，使用第59年重启nc文件进行重启
```shell
./create_newcase --case b1850_tx_maritime_h2_220725 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_maritime_h2_220725
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_tx_maritime_h1_220721
./xmlchange RUN_REFDATE=0059-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=30
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_maritime_h1_220721/user_nl_cam .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_maritime_h1_220721/sbatch1.sh .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_maritime_h1_220721/user_nl_mom .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_maritime_h1_220721/user_nl_cice .
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

## (三) 控制实验的重启

实验名 b1850_control4_220624 享年 0097

```shell
./create_newcase --case b1850_control_h1_220702 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_control_h1_220702
./xmlchange NTASKS=-50
./xmlchange RUN_REFCASE=b1850_control4_220624
./xmlchange RUN_REFDATE=0097-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=3
./xmlchange REST_N=3
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control4_220624/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control4_220624/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control4_220624/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control4_220624/user_nl_cice .

./case.build --skip-provenance-check

cp b1850_control4_220624/run/*.r.* b1850_control_h1_220702/run/
cp b1850_control4_220624/run/*.rs.* b1850_control_h1_220702/run/
cp b1850_control4_220624/run/*rpo* b1850_control_h1_220702/run/
cp b1850_control4_220624/run/*.i.* b1850_control_h1_220702/run/
```

## (四)无印度大陆实验的重启
<font color=red>跑到第85年左右断了，这里再续个三十年spinup</font>

```shell
./create_newcase --case b1850_tx_indian_h2_220731 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_indian_h2_220731
./xmlchange NTASKS=-40
./xmlchange RUN_REFCASE=b1850_tx_indian_h1_220726
./xmlchange RUN_REFDATE=0085-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=12
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/user_nl_cam .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/sbatch1.sh .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/user_nl_mom .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/user_nl_cice .
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

cp b1850_tx_indian_h1_220726/run/*.r.*85* b1850_tx_indian_h2_220731/run/
cp b1850_tx_indian_h1_220726/run/*.rs.*85* b1850_tx_indian_h2_220731/run/
cp b1850_tx_indian_h1_220726/run/*rpo*85* b1850_tx_indian_h2_220731/run/
cp b1850_tx_indian_h1_220726/run/*.i.*85* b1850_tx_indian_h2_220731/run/
```

# SPIN UP 后的正式实验

（1）control

```
./create_newcase --case b1850_control_o1_220703 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_control_o1_220703
./xmlchange NTASKS=-32
./xmlchange RUN_REFCASE=b1850_control_h1_220702
./xmlchange RUN_REFDATE=0004-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=25
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_h1_220702/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_h1_220702/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_h1_220702/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_h1_220702/user_nl_cice .

./case.build --skip-provenance-check

cp b1850_control_h1_220702/run/*.r.* b1850_control_o1_220703/run/
cp b1850_control_h1_220702/run/*.rs.* b1850_control_o1_220703/run/
cp b1850_control_h1_220702/run/*rpo* b1850_control_o1_220703/run/
cp b1850_control_h1_220702/run/*.i.* b1850_control_o1_220703/run/
```

(2)   global_1m

```
./create_newcase --case b1850_global1m_o1_220703 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global1m_o1_220703
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_global_1m_220620
./xmlchange RUN_REFDATE=0099-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=25
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_220620/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_220620/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_220620/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global_1m_220620/user_nl_cice .

./case.build --skip-provenance-check

cp b1850_global_1m_220620/run/*.r.* b1850_global1m_o1_220703/run/
cp b1850_global_1m_220620/run/*.rs.* b1850_global1m_o1_220703/run/
cp b1850_global_1m_220620/run/*rpo* b1850_global1m_o1_220703/run/
cp b1850_global_1m_220620/run/*.i.* b1850_global1m_o1_220703/run/
```

<font color=red>这里我第一次RUN_REFDATE写错了，我直接改了这个值不需要./case.setup --reset和重新编译，直接提交就好了</font>

2022-7-3: 笑死，branch后的第二年就崩了，重新hybrid吧。

```shell
./create_newcase --case b1850_global1m_o2_220703 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global1m_o2_220703
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_global_1m_220620
./xmlchange RUN_REFDATE=0099-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=26
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o1_220703/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o1_220703/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o1_220703/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o1_220703/user_nl_cice .

./case.build --skip-provenance-check

cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o1_220703/run/*.r.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o1_220703/run/*.rs.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o1_220703/run/*rpo* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o1_220703/run/*.i.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/
```

<font color=red>I do not know why it stop at 0029 years,here I need to restart it using branch run</font>

```shell
./create_newcase --case b1850_global1m_o3_220711 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global1m_o3_220711
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_global1m_o2_220703
./xmlchange RUN_REFDATE=0029-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=14
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o2_220703/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o2_220703/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o2_220703/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_global1m_o2_220703/user_nl_cice .

./case.build --skip-provenance-check

cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.r.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.rs.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.i.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
```

 由于我错把lym服务器清空了，所幸global 1m的实验restart场得以保留，因此在wgx上重启1m的控制实验
```shell
./create_newcase --case b1850_global1m_o1_220726 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_global1m_o1_220726
./xmlchange NTASKS=-46
./xmlchange RUN_REFCASE=b1850_global_1m_220620
./xmlchange RUN_REFDATE=0099-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=30
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_o1_220703/user_nl_cam .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_o1_220703/sbatch1.sh .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_o1_220703/user_nl_mom .
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_control_o1_220703/user_nl_cice .

./case.build --skip-provenance-check

cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.r.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.rs.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
cp /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o2_220703/run/*.i.* /public1/home/lym/swh/cesm2.1.3/scratch/b1850_global1m_o3_220711/run/
```






(3) indian experiment

<font color=red>Attention: previous experiment has interrupted, so the official experiment is hybrid reboot</font>

```shell
./create_newcase --case b1850_tx_indian_o1_220706 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_indian_o1_220706
./xmlchange NTASKS=-40
./xmlchange RUN_REFCASE=b1850_tx_indian_220627
./xmlchange RUN_REFDATE=0059-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=27
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx_indian_220627/user_nl_cam .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx_indian_220627/sbatch1.sh .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx_indian_220627/user_nl_mom .
cp /public1/home/lym/swh/cesm2.2.0/cime/scripts/b1850_tx_indian_220627/user_nl_cice .
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

cp b1850_tx_indian_220627/run/*.r.* b1850_tx_indian_o1_220706/run/
cp b1850_tx_indian_220627/run/*.rs.* b1850_tx_indian_o1_220706/run/
cp b1850_tx_indian_220627/run/*rpo* b1850_tx_indian_o1_220706/run/
cp b1850_tx_indian_220627/run/*.i.* b1850_tx_indian_o1_220706/run/
```

<font color=red>2022-7-26重新跑的印度大陆实验，还在spinup的阶段，已经运行了59年，但是我忘记把地形给抹去了，所以重开一个然后把地形抹去</font>

```shell
./create_newcase --case b1850_tx_indian_h1_220726 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_indian_h1_220726
./xmlchange NTASKS=-40
./xmlchange RUN_REFCASE=b1850_tx_indian_h0_220718
./xmlchange RUN_REFDATE=0059-01-01
./xmlchange RUN_TYPE=branch
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=25
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h0_220718/user_nl_cam .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h0_220718/sbatch1.sh .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h0_220718/user_nl_mom .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h0_220718/user_nl_cice .
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

cp b1850_tx_indian_h0_220718/run/*.r.* b1850_tx_indian_h1_220726/run/
cp b1850_tx_indian_h0_220718/run/*.rs.* b1850_tx_indian_h1_220726/run/
cp b1850_tx_indian_h0_220718/run/*rpo* b1850_tx_indian_h1_220726/run/
cp b1850_tx_indian_h0_220718/run/*.i.* b1850_tx_indian_h1_220726/run/
```

(4) maritime experiment
<font color=red>2022-7-30海洋性大陆实验的spinup基本完成了，接下来开始跑正式实验</font>

```shell
./create_newcase --case b1850_tx_maritime_o1_220730 --res f09_t061 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850_tx_maritime_o1_220730
./xmlchange NTASKS=-36
./xmlchange RUN_REFCASE=b1850_tx_maritime_h2_220725
./xmlchange RUN_REFDATE=0095-01-01
./xmlchange RUN_TYPE=hybrid
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=28
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
cp /public1/home/wgx/swh/cesm2.2.0/cime/scripts/b1850_global1m_o1_220726/user_nl_cam .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/sbatch1.sh .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/user_nl_mom .
cp /public1/home/lym/swh/cesm/cime/scripts/b1850_tx_indian_h1_220726/user_nl_cice .
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

cp b1850_tx_maritime_h2_220725/run/*.r.* b1850_tx_maritime_o1_220730/run/
cp b1850_tx_maritime_h2_220725/run/*.rs.* b1850_tx_maritime_o1_220730/run/
cp b1850_tx_maritime_h2_220725/run/*rpo* b1850_tx_maritime_o1_220730/run/
cp b1850_tx_maritime_h2_220725/run/*.i.* b1850_tx_maritime_o1_220730/run/
```



# 重启记录

因为更改海陆分布实验还是会断掉，所以要记录下断点时间，方便后续拼接

## 无印度大陆实验

1. 实验名 b1850_tx6_indian_220622      实验年份0-63年
2. 实验名 b1850_tx_indian_220627         实验年份起始：63



## 无海洋性大陆实验

1. 实验名b1850_tx4_maritime_220624  实验年份0~28年
