;2021/8/4
;更改地形数据
begin
f = addfile("/public1/home/lym/swh/cesm2.1.3/inputdata/atm/cam/topo/fv_0.9x1.25_nc3000_Nsw042_Nrs008_Co060_Fi001_ZR_sgh30_24km_GRNL_c170103.nc","r")
f_a = f->PHIS
f_b = f->LANDFRAC
f_c = f->SGH
f_d = f->SGH30
f_e = f->LANDM_COSLAT
f_f = f->lat
f_g = f->lon
f_h = f->TERR_UF
f_i = f->SGH_UF
f_j = f->GBXAR
f_k = f->MXDIS
f_l = f->RISEQ
f_m = f->FALLQ
f_n = f->MXVRX
f_o = f->MXVRY
f_p = f->ANGLL
f_q = f->ANGLX
f_r = f->ANISO
f_s = f->ANIXY
f_t = f->HWDTH
f_u = f->WGHTS
f_v = f->CLNGT
f_w = f->CWGHT
f_x = f->COUNT

f_a({8:23},{90:110})  =  where(f_b({8:23},{90:110}).ne.0 ,  10 ,   f_a({8:23},{90:110}) )

fout = addfile("/public1/home/lym/swh/cesm2.1.3/inputdata/atm/cam/topo/topo_1m_indo.nc","c")

fout->PHIS                =             f_a
fout->LANDFRAC            =             f_b
fout->SGH                 =             f_c
fout->SGH30               =             f_d
fout->LANDM_COSLAT        =             f_e
fout->lat                 =             f_f
fout->lon                 =             f_g
fout->TERR_UF             =             f_h
fout->SGH_UF              =             f_i
fout->GBXAR               =             f_j
fout->MXDIS               =             f_k
fout->RISEQ               =             f_l
fout->FALLQ               =             f_m
fout->MXVRX               =             f_n
fout->MXVRY               =             f_o
fout->ANGLL               =             f_p
fout->ANGLX               =             f_q
fout->ANISO               =             f_r
fout->ANIXY               =             f_s
fout->HWDTH               =             f_t
fout->WGHTS               =             f_u
fout->CLNGT               =             f_v
fout->CWGHT               =             f_w
fout->COUNT               =             f_x

end
