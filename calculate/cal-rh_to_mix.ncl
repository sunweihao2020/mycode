;2020/12/15
;merra2合成分析：湿度
;将湿度转化为混合比
;所用函数：
;http://www.ncl.ucar.edu/Document/Functions/Built-in/mixhum_ptrh.shtml
begin
f  =  addfile("/data5/2019swh/data/composite_rh.nc","r")
lev = f->level
rh  = f->RH
f2 = addfile("/data5/2019swh/data/composite3.nc","r")
t   = f2->T
w   = t
;do tttt = 0,60
;    do xxxx = 0,575
;        do yyyy = 0,360
;            w(tttt,:,yyyy,xxxx) = mixhum_ptrh(lev,t(tttt,:,yyyy,xxxx),rh(tttt,:,yyyy,xxxx),1)
;        end do
;    end do
;end do
rh = rh*100
lev_con  = conform_dims(dimsizes(rh), lev, (/1/))
copy_VarCoords(rh, lev_con)
printVarSummary(lev_con)
w        = mixhum_ptrh(lev_con,t,rh,1)
printVarSummary(w)

;print(w(:,:,{30},{110}))
;exit
fout = addfile("/data5/2019swh/data/composite_mix_ratio.nc","c")
filedimdef(fout, "time", -1, True)
w@units = "kg/kg"
fout->mix_ratio = w


end
