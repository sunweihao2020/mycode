;2020/12/16
;merra2合成分析资料
;计算对流凝结高度
begin
system("rm -rf /data5/2019swh/data/composite_tlcl.nc")
f  =  addfile("/data5/2019swh/data/","r")
mx = f->mix_ratio
lev  = f->level
f2 = addfile("/data5/2019swh/data/composite3.nc","r")
t   = f2->T

;do tttt = 0,60
;    do xxxx = 0,575
;        do yyyy = 0,360
;            w(tttt,:,yyyy,xxxx) = mixhum_ptrh(lev,t(tttt,:,yyyy,xxxx),rh(tttt,:,yyyy,xxxx),1)
;        end do
;    end do
;end do
lev_con  = conform_dims(dimsizes(mx), lev, (/1/))
copy_VarCoords(mx, lev_con)
printVarSummary(lev_con)
w        = tlcl_mixr_bolton(t, mx, lev_con, (/1,0,0,1/))
printVarSummary(w)
copy_VarCoords(mx, w)

fout = addfile("/data5/2019swh/data/composite_tlcl.nc","c")
filedimdef(fout, "time", -1, True)
w@units = "K"
fout->tlcl = w


end