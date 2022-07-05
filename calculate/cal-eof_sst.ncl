;2021/7/14
;本代码计算35年季风爆发前两个星期及前一个星期的海温eof分解
begin
f = addfile("/data5/2019swh/data/burst_seris/composite_sst.nc","r")
sst =  f->sea_surface_temperature(:,16,:,:)           ;这里我只读取-14day

;计算权重
w   =  sqrt(cos(0.01745329*sst&lat))
wp  =  sst*conform(sst,w,1)
copy_VarCoords(sst, wp)   ;这里应该是权重换算过的海温

;;计算eof
sst_t  =  wp(lat|:,lon|:,year|:)
neof   =  2
eof    =  eofunc_Wrap(sst_t, neof, False)

;;north 检验
