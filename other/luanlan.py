import numpy as np
import math
a=np.loadtxt('/Users/sunweihao/data/other/tmean.txt')
t=a[:,3:21]
date=a[:,0:3]
exp = 1.8 * t
base = 1.07
mc = exp.copy()
for i in range(15580):
    for j in range(18):
        mc[i,j] = 0.254 * math.pow(base,exp[i,j])