---
title: cesm2.2.0使用
date: 2022-06-06 14:31:40
tags: CESM
---

c

测试cesm2.2

```
./create_newcase --case control1 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd control1
```

```
./create_newcase --case control_30 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd control_30
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup --skip-provenance-check
```



# 220608测试 FHIST

```
./create_newcase --case test2_2_1 --res f09_g17 --compset FHIST --run-unsupported --compiler intel --mach oneapi
cd test2_2_1
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
./case.build --skip-provenance-check
```



# 220608测试 b1850m

```
./create_newcase --case b1850m2 --res f09_g17 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd test2_2_1
./xmlchange NTASKS=-16
./xmlchange STOP_OPTION=nyears
./xmlchange STOP_N=2
./xmlchange RESUBMIT=10
./xmlchange REST_N=2
./xmlchange REST_OPTION=nyears
./case.setup
./case.build --skip-provenance-check
```

# 20220610测试 b1850m 已经下载完文件，看下能不能跑控制实验

```
./create_newcase --case b1850m2 --res f09_g16 --compset B1850MOM --run-unsupported --compiler intel --mach oneapi
cd b1850m2
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

