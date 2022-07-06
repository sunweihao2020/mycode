begin
f = addfile("/data5/2019swh/data/composite_shlh.nc","r")
f2 = addfile("/data5/2019swh/data/land_and_ocean.nc","r")
sh = f->SSHF
sh = -sh/3600/24
lh = f->SLHF
lh = -lh/3600/24
lsm = short2flt(f2->lsm(0,:,:))

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
plot1 = new(15,graphic)
plot2 = new(15,graphic)
plot3 = new(15,graphic)
plot4 = new(15,graphic)
dum1   = new(15,graphic)
dum2   = new(15,graphic)
dum3   = new(15,graphic)
dum4   = new(15,graphic)
wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/lh_ocean")
wks2 = gsn_open_wks("pdf","/data5/2019swh/paint/day/lh_land")
wks3 = gsn_open_wks("pdf","/data5/2019swh/paint/day/sh_ocean")
wks4 = gsn_open_wks("pdf","/data5/2019swh/paint/day/sh_land")

do day = 4,33,2
    land1 = lh(day,:,:)
    land1 = mask(lh(day,:,:),(lsm .gt. 0.1),1)
    land2 = sh(day,:,:)
    land2 = mask(sh(day,:,:),(lsm .gt. 0.1),1)
    
    ocean1 = lh(day,:,:)
    ocean1 = mask(lh(day,:,:),lsm,0)
    ocean2 = sh(day,:,:)
    ocean2 = mask(sh(day,:,:),lsm,0)
    
    ;gsn_define_colormap(wks,"temp_19lev")
    res = True
    res@gsnDraw               = False
    res@gsnFrame              = False
    res@cnFillOn              = True     ; turn on color fill
    res@cnFillPalette         = "MPL_OrRd"
    res@cnLineLabelsOn        = False
    res@lbLabelBarOn          = False 
    res@cnLevelSelectionMode       = "ExplicitLevels" 
    res@mpMinLatF            = -30      ; range to zoom in on
    res@mpMaxLatF            =  30.
    res@mpMinLonF            =  30.
    res@mpMaxLonF            = 120.
    res@gsnRightString       = "W/M**2 "
    res@gsnStringFont         = 2
    res@tmYLLabelFontHeightF      = 0.024
    res@tmXBLabelFontHeightF      = 0.024

    res@gsnLeftString         = char_day(day)
    ;res@tmYLLabelDeltaF = -0.6  ;坐标值跑出去了就调这个

    res@cnLevels             := ispan(120,300,20)


    plot1((day-4)/2) = gsn_csm_contour_map(wks1,ocean1(:,:), res) 
    plot2((day-4)/2) = gsn_csm_contour_map(wks2,land1(:,:), res) 
    res@cnLevels             := ispan(0,100,10) 
    res@mpMinLatF            = -10 
    res@mpMaxLatF            =  30.
    plot3((day-4)/2) = gsn_csm_contour_map(wks3,ocean2(:,:), res) 
    res@cnLevels             := ispan(20,120,20) 
    plot4((day-4)/2) = gsn_csm_contour_map(wks4,land2(:,:), res)  

  
    polyres                   = True
    polyres@gsLineColor       = "black"
    polyres@gsLineThicknessF  = 3
    polyres@gsLineDashPattern = 2
    dum1((day-4)/2) = gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum2((day-4)/2) = gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum3((day-4)/2) = gsn_add_polyline(wks3, plot3((day-4)/2), (/30,120/), (/0,0/), polyres)
    dum4((day-4)/2) = gsn_add_polyline(wks4, plot4((day-4)/2), (/30,120/), (/0,0/), polyres)


end do
pnlres = True
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
pnlres@gsnPanelMainString = "latent heat flux"
gsn_panel(wks1,plot1,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "latent heat flux"
gsn_panel(wks2,plot2,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "sensible heat flux"
gsn_panel(wks3,plot3,(/5,3/),pnlres)
pnlres@gsnPanelMainString = "sensible heat flux"
gsn_panel(wks4,plot4,(/5,3/),pnlres)
end