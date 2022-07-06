;2021/6/14
;本代码根据地转偏差资料绘制：地转偏差绝对值、角度
;相比于1，这里绝对值用阴影，角度叠加到上面用等值线
begin 
f1 = addfile("/data5/2019swh/data/geostrophic_deviation.nc","r")
deviation =    f1->deviation
cosu      =    f1->cosu
u         =    f1->u_deviation
v         =    f1->v_deviation


deviation  =  where(abs(deviation).ge.100,deviation@_FillValue,deviation)

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

;绘制地转偏差的设置
res = True
res@cnFillOn              = True   ; turn on color fill
res@gsnDraw               = False
res@gsnFrame              = False
res@gsnAddCyclic          = False
res@gsnStringFont         = 2

res@mpMinLatF            =  5 
res@mpMaxLatF            =  30.
res@mpMinLonF            =  60.
res@mpMaxLonF            =  120.



res@cnLineLabelsOn        = False 
res@cnInfoLabelOn         = False 
res@cnLinesOn             = False 
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels              = fspan(0,10,6)
res@cnFillColors          = (/2,30,100,145,170,193,226/)
res@cnLineLabelsOn       = False
res@cnLineLabelFontAspectF = 2

res@lbLabelBarOn         = False 

res@vpWidthF              = 0.6
res@vpHeightF             = 0.55

res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024

level = (/925,850,700,500,300,200/)
levels = (/"925hPa","850hPa","700hPa","500hPa","300hPa","200hPa"/)


;绘制角度的设置
res1 = True
res1@cnFillOn              = False   ; turn on color fill
res1@gsnDraw               = False
res1@gsnFrame              = False
res1@gsnAddCyclic          = False
res1@gsnStringFont         = 2
res1@gsnContourNegLineDashPattern = 1


res1@cnInfoLabelOn         = False 
res1@cnLinesOn             = True 
res1@cnLevelSelectionMode       = "ExplicitLevels" 
res1@cnLevels              = (/-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1/)



do yy = 22,33
    wks1  =  gsn_open_wks("pdf","/data5/2019swh/paint/day/geostrophic_deviation_"+char_day(yy))
    gsn_define_colormap(wks1,"cmocean_amp")
    plot1 =  new(6,graphic)
    plot2 =  new(6,graphic)
    do ll = 0,5
        res@gsnLeftString   =      levels(ll)
        res@gsnRightString  =      char_day(yy)
        plot1(ll) = gsn_csm_contour_map(wks1, deviation(yy,{level(ll)},:,:), res)
        ;plot2(ll) = gsn_csm_contour(wks1, cosu(yy,{level(ll)},:,:), res1)
        ;overlay(plot1(ll),plot2(ll))
    end do
pnlres = True
pnlres@gsnPanelMainString = "geostrophic deviation & angle(cosu)"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/2,3/),pnlres)
end do
end
