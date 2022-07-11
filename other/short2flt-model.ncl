;2021/1/19
;将short型model数据转换为float
;时间跨度：数据有残缺，25年
;资料：era5
begin
path0 = "/data5/2019swh/mydown/era5-model/"
path1 = "/data5/2019swh/mydown/era5-model/"
year = (/1982,1985,1986,1987,1988,1989,1990,1991,1992,1993,1994,1996,1998,1999,2000,2001,2002,2003,2004,2005,2006,2007,2008,2012,2013,2014,2015,2016,2017,2018/)
do yyyy=0,29
    f1 = addfile(path0+year(yyyy)+".nc","r")



    v1 := short2flt(f1->t)
    v2 := short2flt(f1->w)

    v3 := short2flt(f1->vo)
    v4 := short2flt(f1->mttpm)
    v6 := short2flt(f1->u)
    v7 := short2flt(f1->v)



    fout1 = addfile(path1+year(yyyy)+"_float.nc","c")

    filedimdef(fout1, "time", -1, True)
    fout1->t = v1
    fout1->w = v2
    fout1->vo = v3
    fout1->mttpm = v4
    fout1->u = v6
    fout1->v = v7

    delete(fout1)

    delete(f1)



end do
end