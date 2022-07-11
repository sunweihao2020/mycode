;2020/11/29
;将short型oisst转换为float
;时间跨度：1982-2016
begin
path0 = "/data1/OISST/daily/"
path2 = "/data5/2019swh/data/OISST/"

do yyyy=2014,2016
    path1 = path0+yyyy+"/AVHHR/"
    files := systemfunc("ls "+path1+"*only*.nc")
    do i =0,364
        f = addfile(files(i),"r")
        sst = short2flt(f->sst(0,0,:,:))
        fout = addfile(path2+yyyy+"_"+(i+1)+".nc","c")
        filedimdef(fout, "time", -1, True)

        fout->sst = sst
        delete(fout)
        delete(f)
    end do
end do
end