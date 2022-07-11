#!/bin/bash
for ((yr=1980;yr<=2019;yr++));do
    year=$(printf "%04d" ${yr})
    cat  /home/admin/mycode/down/down-era5-single/down-era5-single.py | sed 's/yyyy/'${year}'/g' > /home/admin/mycode/down/down-era5-single/down-era5-single-${year}.py
    nohup python down-model-${year}.py &
done