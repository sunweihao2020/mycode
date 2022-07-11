;2020/11/30
;将short型oisst转换为float
;时间跨度：1980-2018
;资料：era-interim
begin
path0 = "/home/sun/downdata/era-interim/"
path1 = "/home/sun/downdata/era-interim/u10/"


do yyyy=1980,2018
    f1 = addfile(path0+"U10m."+yyyy+".00.nc","r")
    f2 = addfile(path0+"U10m."+yyyy+".06.nc","r")
    f3 = addfile(path0+"U10m."+yyyy+".12.nc","r")
    f4 = addfile(path0+"U10m."+yyyy+".18.nc","r")
    f5 = addfile(path0+"V10m."+yyyy+".00.nc","r")
    f6 = addfile(path0+"V10m."+yyyy+".06.nc","r")
    f7 = addfile(path0+"V10m."+yyyy+".12.nc","r")
    f8 = addfile(path0+"V10m."+yyyy+".18.nc","r")

    v1 = short2flt(f1->u10)
    v2 = short2flt(f2->u10)
    v3 = short2flt(f3->u10)
    v4 = short2flt(f4->u10)
    v5 = short2flt(f5->v10)
    v6 = short2flt(f6->v10)
    v7 = short2flt(f7->v10)
    v8 = short2flt(f8->v10)

    v9 = (v1+v2+v3+v4)/4
    v10 = (v5+v6+v7+v8)/4
    copy_VarCoords(v1, v9)
    copy_VarCoords(v5, v10)

    fout1 = addfile(path1+"u10_"+yyyy+"_.nc","c")
    fout2 = addfile(path1+"v10_"+yyyy+"_.nc","c")
    filedimdef(fout1, "time", -1, True)
    filedimdef(fout2, "time", -1, True)
    fout1->u10 = v9
    fout2->v10 = v10
    delete(fout1)
    delete(fout2)
    delete(f1)
    delete(f2)
    delete(f3)
    delete(f4)
    delete(f5)
    delete(f6)
    delete(f7)
    delete(f8)

end do
end