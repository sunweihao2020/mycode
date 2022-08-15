'''
2022-8-3
This script is used to check regional meridional stream function I calculated
'''
import os
import numpy as np
import sys
import xarray as xr
import matplotlib.pyplot as plt
sys.path.append("/home/sun/mycode/module/")
sys.path.append("/home/sun/mycode_git/paint/")
from module_sun import *
import sys
from matplotlib import cm
from matplotlib.colors import ListedColormap
from paint_lunwen_version3_0_fig2a_tem_gradient_20220426 import add_text

