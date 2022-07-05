;2020/12/16
;merra2合成分析资料
;计算相当位温
begin
system("rm -rf /data5/2019swh/data/composite_equivalent_tem.nc")
f  =  addfile("/data5/2019swh/data/composite_mix_ratio.nc","r")
mx = f->mix_ratio
lev  = f->level
f2 = addfile("/data5/2019swh/data/composite3.nc","r")
t   = f2->T
w   = t

f3 = addfile("/data5/2019swh/data/composite_tlcl.nc","r")
tlcl = f3->tlcl


lev_con  = conform_dims(dimsizes(mx), lev, (/1/))
copy_VarCoords(mx, lev_con)
printVarSummary(lev_con)
w        = pot_temp_equiv_tlcl(lev_con, t, tlcl, mx, (/0,1,0,1/))
printVarSummary(w)
copy_VarCoords(mx, w)

fout = addfile("/data5/2019swh/data/composite_equivalent_tem.nc","c")
filedimdef(fout, "time", -1, True)
w@units = "K"
fout->theate_e = w


end