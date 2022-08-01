; 2022/7/31
; This code calculate divergent wind in the global range
; based on composite3.nc
begin
    path0  =  "/home/sun/data/composite/"
    f0  =  addfile(path0+"composite3.nc","r")
    f1  =  addfile(path0+"composite_PS.nc","r")

    ps    =  f1->PS
    u     =  f0->uwind
    v     =  f0->vwind

    lat   =  f0->lat
    lon   =  f0->lon
    level =  f0->level

    level =  level * 100
    level@units  =  "Pa"

    dd    =  new((/61,42,361,576/),double)
    dv    =  new((/2,61,42,361,576/),double)

    ; fill missing value with zero
    u     =  where(ismissing(u),0,u)
    v     =  where(ismissing(v),0,v)

    ; first process using u and v
    i = 0
    do ll = 0,41
        do day = 0,60
            print(i)
            dd(day,ll,:,:)   = uv2dv_cfd(u(day,ll,:,:), v(day,ll,:,:), lat, lon, 2)
            dv(:,day,ll,:,:) = dv2uvF(dd(day,ll,:,:))
            i = i+1
        end do
    end do

    dv_v  =  dv(1,:,:,:,:)
    dv_u  =  dv(0,:,:,:,:)

    setfileoption("nc","Format","LargeFile")
    fout = addfile(path0+"composite_divergent_wind_220731.nc","c")
  
    filedimdef(fout,"time",-1,True)
    fout->divergent_u  =  dv_u
    fout->divergent_v  =  dv_v

    fileatt  =  True
    fileatt@time  =  "2022-7-31"
    fileatt@description  =  "This file includes divergent wind calculated based on composite3.nc"  

end
