'''
2021/9/16
本代码计算并绘制上层温度的经向-纬度图，对应数据为庄的三个实验及控制实验
'''
import os
import xarray as xr
import numpy as np
import math

base1  =  xr.open_dataset("/data5/2019swh/data/zhuang_plev/plev_icid_T.nc")

def cal_upper_average():
    #本代码计算上层的温度
