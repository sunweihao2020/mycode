;2022/6/9
;更改地形数据,全球1m
begin
f = addfile("/home/sun/data/cesm/fv_0.9x1.25_nc3000_Nsw042_Nrs008_Co060_Fi001_ZR_sgh30_24km_GRNL_c170103.nc","r")
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

lat = f->lat
lon = f->lon

do dim1 = 0,(192-1)
    do dim2 = 0,(288-1)
        if (lat(dim1) .ge. -10 .and. lat(dim1) .le. 6 .and. lon(dim2) .ge. (95) .and. lon(dim2) .le. (100)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 3 .and. lon(dim2) .ge. (100) .and. lon(dim2) .le. (101)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 2.2 .and. lon(dim2) .ge. (101) .and. lon(dim2) .le. (102)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 1.7 .and. lon(dim2) .ge. (102) .and. lon(dim2) .le. (103)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 1.25 .and. lon(dim2) .ge. (103) .and. lon(dim2) .le. (104)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 1.25 .and. lon(dim2) .ge. (104) .and. lon(dim2) .le. (105)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 5 .and. lon(dim2) .ge. (105) .and. lon(dim2) .le. (110)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 15 .and. lon(dim2) .ge. (110) .and. lon(dim2) .le. (120)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 20 .and. lon(dim2) .ge. (120) .and. lon(dim2) .le. (130)) .or. (lat(dim1) .ge. -10 .and. lat(dim1) .le. 10 .and. lon(dim2) .ge. (130) .and. lon(dim2) .le. (160)) then
            f_a(dim1,dim2) = 0
            f_b(dim1,dim2) = 0
        end if
    end do
end do

wks  = gsn_open_wks("png","/home/sun/paint/change_land_mask/cam_topo_tx66_maritime")            ; send graphics to PNG file
res                      = True                 ; plot mods desired
res@gsnDraw              = False                ; don't draw yet
res@gsnFrame             = False                ; don't advance frame yet
res@cnFillOn             = True                 ; turn on color fill
res@cnLinesOn            = False                ; turn off contour lines
res@cnLineLabelsOn       = False                ; turn off contour line labels
;res@cnLevelSelectionMode       = "ExplicitLevels"
;res@cnLevels             = fspan(0,60,61)
plot = gsn_csm_contour(wks,f_c,res)  
draw(plot)
frame(wks)
sys       =    systemfunc("rm /home/sun/data/cesm/topo_no_maritime.nc")
fout = addfile("/home/sun/data/cesm/topo_no_maritime.nc","c")

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
