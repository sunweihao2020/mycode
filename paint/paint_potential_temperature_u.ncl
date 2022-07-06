;2021/4/27
;所用资料：merra2季风爆发的合成分析
;要素：位温，u
;层次：多层次
load "/data5/2019swh/mycode/calculate/add_TP.ncl"
begin
f1 = addfile("/data5/2019swh/data/potential_temperature.nc", "r")
f2 = addfile("/data5/2019swh/data/composite3.nc","r")
u = f2->uwind
pt = f1->pt

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)

u_a = dim_avg_n_Wrap(u(:,:,:,{90:95}), 3)
t_a = dim_avg_n_Wrap(pt(:,:,:,{90:95}), 3)

res = True
res@gsnDraw               = False
res@gsnFrame              = False
res@cnFillOn              = True     
res@cnLineLabelsOn        = False
res@lbLabelsOn            = False
res@lbLabelBarOn          = False
res@cnLinesOn             = False
res@cnLevelSelectionMode       = "ExplicitLevels" 
res@cnLevels             = fspan(-10,10,11)
res@cnFillColors         = (/2,3,4,5,6,7,13,14,15,16,17,18/)
res@gsnRightString       = "m/s"

res@gsnStringFont         = 2
res@tmYLLabelFontHeightF      = 0.024
res@tmXBLabelFontHeightF      = 0.024
res@cnInfoLabelOn         = False

res1 = True
res1@gsnDraw               = False
res1@gsnFrame              = False
res1@cnFillOn              = False     
res1@cnLineLabelsOn        = False
res1@lbLabelsOn            = False
res1@lbLabelBarOn          = False
res1@cnLinesOn             = True
res1@cnLevelSpacingF       = 4
res1@cnInfoLabelOn         = False

plot1 = new(15,graphic)
dum1 = new(15,graphic)

wks1 = gsn_open_wks("pdf","/data5/2019swh/paint/day/u_pt")
gsn_define_colormap(wks1,"BlueDarkRed18")

do day = 16,30
plot1(day-16) = gsn_csm_pres_hgt(wks1, u_a(day,{1000:200},{-10:40}), res )
a = gsn_csm_pres_hgt(wks1, t_a(day,{1000:200},{-10:40}),res1)
overlay(plot1(day-16),a)
dum1(day-16) = overlay_x_latitude(wks1,plot1(day-16),93,"black")
end do

pnlres = True
pnlres@gsnPanelMainString = "u-wind & potential temperature"
pnlres@gsnPanelLabelBar  = True
pnlres@gsnPanelDebug     = True     ; To get information from panel
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
gsn_panel(wks1,plot1,(/3,5/),pnlres)


end