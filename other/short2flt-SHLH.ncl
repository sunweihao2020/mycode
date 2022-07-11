;2020/12/1
;将short型SHLH转换为float
;时间跨度：1980-2018
;资料：era-interim
begin
path0 = "/home/sun/downdata/era-interim/"
path1 = "/home/sun/downdata/era-interim/shlh/"

do yyyy=1980,2018
    f1 = addfile(path0+"SH."+yyyy+".00.nc","r")
    f2 = addfile(path0+"SH."+yyyy+".12.nc","r")

    f3 = addfile(path0+"LH."+yyyy+".00.nc","r")
    f4 = addfile(path0+"LH."+yyyy+".12.nc","r")


    v1 := short2flt(f1->sshf)
    v2 := short2flt(f2->sshf)

    v3 := short2flt(f5->slhf)
    v4 := short2flt(f6->slhf)


    v5 := (v1+v2)
    v6 := (v3+v4)
    copy_VarCoords(v1, v5)
    copy_VarCoords(v3, v6)

    fout1 = addfile(path1+"sh_"+yyyy+"_.nc","c")
    fout2 = addfile(path1+"lh_"+yyyy+"_.nc","c")
    filedimdef(fout1, "time", -1, True)
    filedimdef(fout2, "time", -1, True)
    fout1->sshf = v5
    fout2->slhf = v6
    delete(fout1)
    delete(fout2)
    delete(f1)
    delete(f2)
    delete(f3)
    delete(f4)


end do
end