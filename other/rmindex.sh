#!/bin/bash

#2020/11/18
#删除下载GPCP时的无关文件
path="/data5/2019swh/mydown/GPCP/"
for k in $( seq 1997 2019 )
do 
rm -rf ${path}${k}/index*
done