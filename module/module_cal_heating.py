'''
2020/12/2
该模块计算总加热率、潜热加热率
公式出自刘伯奇博士论文
'''
import os
import numpy as np
import Ngl, Nio
import json
from geopy.distance import distance
import numpy.ma as ma
import sys
import math
from netCDF4 import Dataset

def all_heating(T,uwind,vwind,pt,omega,dimension):
    #dimension里储存的是维度-（气压/纬度/经度）


    disy = np.array([])
    disx = np.array([])

    p    = dimension[1]
    lat  = dimension[2]
    lon  = dimension[3]
    time = np.arange(61)+1
    T_t = np.gradient(T, time, axis=0)
    #处理坐标信息
    for i in range(0,len(lat)-1):
        disy    =   np.append(disy,distance((lat[i],0),(lat[i+1],0)).m)

    for i in range(0,len(lat)):
        disx    =   np.append(disx,distance((lat[i],lon[0]),(lat[i],lon[1])).m)

    location = np.array([0])
    for dddd in range(0, len(lat)-1):
        location = np.append(location, np.sum(disy[:dddd + 1]))

    T_x = ma.array(ma.zeros(T.shape), mask=T.mask)
    T_y = ma.array(ma.zeros(T.shape), mask=T.mask)

    T_y = np.gradient(T,location,axis = 2)
    for latt in range(0,len(lat)):
        T_x[:,:,latt,:] = np.gradient(T[:,:,latt,:],disx[latt],axis = 2)

    term2 = uwind*T_x+vwind*T_y

    theta_p = np.gradient(pt,p,axis = 1)
    term3 = T
    for pp in range(0,len(p)):
        term3[:,pp,:,:] = math.pow((pp/1000),0.286)*omega[:,pp,:,:]*theta_p[:,pp,:,:]

    term = 1.004*(T_t+term2+term3)         #kJ/(kg K)
    return term,T_t,T_x,T_y

def water_heating(q,uwind,vwind,omega,dimension):
    #dimension里储存的是维度-（气压/纬度/经度）


    disy = np.array([])
    disx = np.array([])

    time = dimension[0]
    p    = dimension[1]
    lat  = dimension[2]
    lon  = dimension[3]

    q_t = np.gradient(q, time, axis=0)
    #处理坐标信息
    for i in range(0,len(lat)-1):
        disy    =   np.append(disy,distance((lat[i],0),(lat[i+1],0)).m)

    for i in range(0,len(lat)):
        disx    =   np.append(disx,distance((lat[i],lon[0]),(lat[i],lon[1])).m)

    location = np.array([0])
    for dddd in range(0, len(lat)-1):
        location = np.append(location, np.sum(disy[:dddd + 1]))

    q_x = ma.array(ma.zeros(q.shape), mask=q.mask)
    q_y = np.gradient(q,location,axis = 2)
    for latt in range(0,len(lat)):
        q_x[:,:,latt,:] = np.gradient(q[:,:,latt,:],disx[latt],axis = 2)

    term2 = uwind*q_x+vwind*q_y

    q_p = np.gradient(q,p,axis = 1)
    term3 = q_p*omega

    term3 = term3 * (60 * 60 * 24)
    term2 = term2 * (60 * 60 * 24)

    term = 2.5e6*(q_t+term2+term3)/1004      #kJ/(kg K)
    return term