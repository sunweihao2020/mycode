; 2022/7/5
; This code calculate regional meridional streamfunction between 90 and 100°E
; based on composite3.nc
begin
    f0  =  addfile("/data5/2019swh/data/composite3.nc","r")
    f1  =  addfile("/data5/2019swh/data/composite_PS.nc","r")

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

    mpsi  =  new((/61,31,361/),double)
    ; calculate mpsi
    j = 0
    do day = 0,60
        print(j)
        mpsi(day,:,:)  =  zonal_mpsi(dv_v(day,1:31:-1,:,432:448), lat, level(1:31:-1), ps(day,:,432:448))
        
        j = j+1
    end do

    ; write to file
    mpsi!0 = "time"
    mpsi!1 = "lev"
    mpsi!2 = "lat"
    mpsi&lev = p(1:31:-1)
    mpsi&lat = lat
    mpsi = mpsi/1E+9

    fout = addfile("/data5/2019swh/data/zonal_meridional_streamfunction_90to100_2.nc","c")
    filedimdef(fout,"time",-1,True)
    fout->MPSI  =  mpsi

    fileatt  =  True
    fileatt@time  =  "2022-7-5"
    fileatt@description  =  "This file generate zonal meridional streamfunction between 90 to 100"  

end
