;2021/2/27
;本代码计算逐层的：的水汽通量、水汽通量散度
;         整层积分的：的水汽通量、水汽通量散度
;使用ncl函数：http://www.ncl.ucar.edu/Document/Functions/Built-in/mixhum_ptrh.shtml

begin
system("rm -rf /data5/2019swh/data/composite_specific_humidity.nc")
f1 = addfile("~/data/composite3.nc","r")
f2 = addfile("~/data/composite_rh.nc","r")

rh = f2->RH
rh = rh*100
t  = f1->T
lev  = f1->level
p  = conform_dims(dimsizes(t), lev, 1)

q  = mixhum_ptrh(p,t,rh,2)
;qq = where(q.gt.0.5 .or. q.lt.0 , q@_FillValue, q)
copy_VarCoords(rh, q)

fout = addfile("~/data/composite_specific_humidity.nc","c")
filedimdef(fout, "time", -1, True)

q@units = "kg/kg"
fout->q = q
end





