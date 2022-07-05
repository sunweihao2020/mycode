import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset

#def get_mask(maskin,maskout):


variables1=['EPV','H','OMEGA','PS','SLP','T','U','V']
variables2=['QV2M','T10M','T2M','TS','U10M','V10M','U2M','V2M']
path='/data1/MERRA2/daily/plev/1985/'
file=Nio.open_file(path+'MERRA2_100.inst3_3d_asm_Np.19851225.SUB.nc')

for i in range(0,8):
    exec(variables1[i]+"=file.variables['"+variables1[i]+"'][:]")
    exec(variables1[i]+"_M=ma.getmaskarray("+variables1[i]+")")

np.savez('/data5/2019swh/data/multi-layer-daily.npz',EPV=EPV_M,H=H_M,OMEGA=OMEGA_M,PS=PS_M,SLP=SLP_M,T=T_M,U=U_M,V=V_M)