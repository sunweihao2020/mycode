#!/bin/bash
for ((yr=1980;yr<=2000;yr++));do
    year=$(printf "%04d" ${yr})
    mkdir ${year}
    cd ${year}
    cat  ../down-multiple-hourly.py  | sed 's/yyyy/'${year}'/g' > ./down-multiple-${year}.py
    nohup python down-multiple-${year}.py &
    cd ..
done
