import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset

path='/data5/2019swh/data/'
f1=Nio.open_file(path+'mean_merra2_1980-2018.nc')


wks_type = "png"
wks = Ngl.open_wks(wks_type,"~/paint/new2")

cnres                 = Ngl.Resources()

# Contour resources
cnres.cnFillOn        = True
cnres.cnFillPalette   = "BlueYellowRed"      # New in PyNGL 1.5.0
cnres.cnLinesOn       = False
cnres.cnLineLabelsOn  = False

# Labelbar resource
cnres.lbOrientation   = "horizontal"

# Scalar field resources
cnres.sfXArray        = lon
cnres.sfYArray        = lat

# Map resources
cnres.mpFillOn               = True
cnres.mpFillDrawOrder        = "PostDraw"
cnres.mpLandFillColor        = "Transparent"
cnres.mpOceanFillColor       = "Transparent"
cnres.mpInlandWaterFillColor = "Transparent"

contour = Ngl.contour_map(wks,T2M[5,:,:],cnres)


