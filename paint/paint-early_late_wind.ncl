;2021/7/1
;本代码绘制早年和晚年的水平环流场图
;早年晚年的选取标准为0.7
begin
path = "/data5/2019swh/data/"
f1 = addfile(path+"early-year-composite.nc","r")
f2 = addfile(path+"late-year-composite.nc", "r")

u1 = f1->u
u2 = f2->u
v1 = f1->v
v2 = f2->v

char_day=(/"D0-30","D0-29","D0-28","D0-27","D0-26","D0-25","D0-24","D0-23","D0-22","D0-21","D0-20","D0-19","D0-18","D0-17","D0-16","D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
lev = (/3,6,12,16,22,24/)
level = (/"925hPa","850hPa","700hPa","500hPa","200hPa","100hPa"/)

vcres                         =      True
vcres@gsnDraw                 =      False             ; do not draw the plot      
vcres@gsnFrame                =      False            ; so we can draw time stamp
vcres@vcRefAnnoOrthogonalPosF =      -1.35             ; move ref vector up
vcres@vpWidthF                =      0.6
vcres@vpHeightF               =      0.55
vcres@gsnAddCyclic            =      False
vcres@vcRefMagnitudeF         =      10 xc====                                                          ; define vector ref mag vcres@vcRefLengthF            =      0.045            ; define length of vec ref
vcres@vcGlyphStyle            =      "CurlyVector"    ; turn on curly vectors
vcres@vcMinDistanceF          =      0.017
vcres@vcRefAnnoOrthogonalPosF =      -1.0   
vcres@vcMinDistanceF          =      0.02
vcres@vcRefLengthF            =      0.03
vcres@vcLineArrowThicknessF   =      1.1
vcres@mpMinLatF               =      -10 
vcres@mpMaxLatF               =      30
vcres@mpMinLonF               =      30
vcres@mpMaxLonF               =      120

polyres                   = True
polyres@gsLineColor       = "black"
polyres@gsLineThicknessF  = 1
polyres@gsLineDashPattern = 2

do ll = 0,5
plot1  =  new(16,graphic)
dum1   =  new(16,graphic)
plot2  =  new(16,graphic)
dum2   =  new(16,graphic)

wks1   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/early_wind"+level(ll))
wks2   =  gsn_open_wks("pdf","/data5/2019swh/paint/day/late_wind"+level(ll))

vcres@gsnRightString          =      level(ll)
    do day = 4,34,2
        vcres@gsnLeftString   =      char_day(day)
        plot1((day-4)/2)      =      gsn_csm_vector_map(wks1,u1(day,lev(ll),:,:),v1(day,lev(ll),:,:),vcres)
        plot2((day-4)/2)      =      gsn_csm_vector_map(wks2,u2(day,lev(ll),:,:),v2(day,lev(ll),:,:),vcres)
        dum1((day-4)/2)       =      gsn_add_polyline(wks1, plot1((day-4)/2), (/30,120/), (/0,0/), polyres)
        dum2((day-4)/2)       =      gsn_add_polyline(wks2, plot2((day-4)/2), (/30,120/), (/0,0/), polyres)
    end do

pnlres = True
pnlres@gsnPanelMainString     =      "early year composite wind at "+level(ll)
pnlres@gsnPanelDebug          =      True     ; To get information from panel
gsn_panel(wks1,plot1,(/4,4/),pnlres)
delete(wks1)
pnlres@gsnPanelMainString     =      "late year composite wind at "+level(ll)
gsn_panel(wks2,plot2,(/4,4/),pnlres)
delete(wks2)
end do
end