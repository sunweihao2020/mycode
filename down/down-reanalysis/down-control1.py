import os
import sys
import urllib
import urllib.request
from pathlib import Path

path1 = "/home/sun/inputlist/"
name  = "control1_inputdata.txt"
with open(path1+name,"r") as f:
    data_list = f.readlines()

data_list1 = []
for lines in data_list:
    url = "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata"
    line1  =  lines.split("=",1)[1]
    line2  =  line1.replace("\n","").split("/",-1)[7:]
    path1  =  "/home/sun/inputdata/control1/"

    for com in line2:
        url   +=  "/"+com

    os.system("wget -c -P "+path1+" --no-check-certificate "+url)
