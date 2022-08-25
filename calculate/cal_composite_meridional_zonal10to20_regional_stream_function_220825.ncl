;2022-08-01
;This code calculate regional streamfunction in the zonal and meridional direction
;The divergent wind using in this script has been already calculated
;The reference including method of regional streamfunction is:https://doi.org/10.1175/JCLI-D-12-00802.1
;reference: https://renqlsysu.github.io/2018/08/08/ncl-dynamical-function/
;Note: zonal range is 90 to 100E
begin
    src_path  =  "/home/sun/data/composite/"

    f1        =  addfile(src_path  +  "composite_PS.nc","r")
    f2        =  addfile(src_path  +  "composite_divergent_wind_220731.nc","r")
    f3        =  addfile(src_path  +  "composite3.nc","r")

    ps_meri   =  f1->PS(:,:,{90:100})
    ps_zonal  =  f1->PS(:,{10:20},:)

    ; f1 do not include lat/lon message, I need to set it

    du        =  f2->divergent_u(:,:,200:220,:)
    dv        =  f2->divergent_v(:,:,:,432:448)

    ; calculate zonal average of above variables
    ps_meri_a      =  dim_avg_n_Wrap(ps_meri, 2)  ; (time,lat)
    ps_zonal_a     =  dim_avg_n_Wrap(ps_zonal,1)  ; (time,lon)

    du_a      =  dim_avg_n_Wrap(du, 2)  ; (time,lev,lon)
    dv_a      =  dim_avg_n_Wrap(dv, 3)  ; (time,lev,lat)

    ; calculate dpres_plevel
    dp_meri   =  dv_a
    dp_zonal  =  du_a
    level     =  f3->level
    ptop      =  0
    iopt      =  0

    ; meridional dp
    do tt = 0,60
        do latt = 0,360
            dp_meri(tt,:,latt)  =  dpres_plevel(level*100,ps_meri_a(tt,latt),ptop,iopt)
        end do
    end do

    ; zonal dp
    do tt = 0,60
        do lonn = 0,575
            dp_zonal(tt,:,lonn)  =  dpres_plevel(level*100,ps_zonal_a(tt,lonn),ptop,iopt)
        end do
    end do

    ; calculate stream function
    g      =   9.8               ; m/(s*s)
    a      =   6378388           ; the radius of earth, m
    pi     =   atan(1.0)*4
    nlev   =   42
    lat    =   f3->lat

    meri_sfm    =  dv_a
    zonal_sfm   =  du_a

    ; calculate meridional function
    do tt  = 0,60,1
        do inl = 0, nlev-1, 1
            meri_sfm(tt,inl,:) = dim_sum_n(dv_a(tt,inl:nlev-1,:)*dp_meri(tt,inl:nlev-1,:),0)
            meri_sfm(tt,inl,:) = meri_sfm(tt,inl,:)*2*pi*cos(lat*pi/180.0)*a/g
        end do
    end do

    ; calculate zonal function
    do tt  = 0,60,1
        do inl = 0, nlev-1, 1
            zonal_sfm(tt,inl,:) = dim_sum_n(du_a(tt,inl:nlev-1,:)*dp_zonal(tt,inl:nlev-1,:),0)
            zonal_sfm(tt,inl,:) = zonal_sfm(tt,inl,:)*2*pi*a/g
        end do
    end do

    ; set coordinate message
    meri_sfm!0  =  "time"
    meri_sfm!1  =  "lev"
    meri_sfm!2  =  "lat"

    zonal_sfm!0  =  "time"
    zonal_sfm!1  =  "lev"
    zonal_sfm!2  =  "lon"

    meri_sfm&time  =  fspan(1,61,61)
    meri_sfm&lev   =  f3->level
    meri_sfm&lat   =  f3->lat

    zonal_sfm&time  =  fspan(1,61,61)
    zonal_sfm&lev   =  f3->level
    zonal_sfm&lon   =  f3->lon
    printVarSummary(meri_sfm)
    printVarSummary(zonal_sfm)

   fout = addfile(src_path+"composite_calculate_regional_streamfunction_zonal10to20_meridional_220825.nc","c")

   filedimdef(fout,"time",-1,True)
   fout->meridional_streamfunction  =  meri_sfm
   fout->zonal_streamfunction       =  zonal_sfm

   fileatt       =  True
   fileatt@time  =  "2022-8-25"
   fileatt@description  =  "This file includes regional streamfunction calculated by me, zonal range is 90 to 100, meridional range is 10 to 20N"  





end