'''
2021/1/24
使用合成的era5数据进行地表位温的计算
使用数据：composite-era5ps.nc composite-modeluv.nc
'''
import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

import os
import numpy as np
import numpy.ma as ma
import Ngl, Nio
from netCDF4 import Dataset
import json
import sys
import time
sys.path.append("/data5/2019swh/mycode/module/")
from module_sun import *
from module_writenc import *
from attribute import *

