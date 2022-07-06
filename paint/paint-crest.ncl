;这波啊，这波是画一下副高脊线;风场位势高度场+脊线
;这里画925、850、700、500、100的 在lev中分别对应3、7、12、16、24
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/contrib/time_axis_labels.ncl"

begin
f = addfile("/data5/2019swh/data/mean_pentad_multilayer_0924.nc", "r")
u = f->uwind
;udx = u
;udy = u
;gradsf(u,udx,udy)
;udy = udy*10e+5
;👆他娘的这种方法不能包含缺测值

;用中央差分算一下梯度吧
udy = center_finite_diff_n(u, 2, False, 0, 2)
uu = u
uu     = where(abs(uu).lt.3.and.udy.gt.0,uu,uu@_FillValue)
v = f->vwind
h = f->H
lat = f->lat
lon = f->lon
lev = f->level
char_pen=(/"p22","p23","p24","p25","p26","p27","p28","p29","p30","p31","p32","p33","p34"/)

do ipen = 1, 13

    wks = gsn_open_wks("pdf", "/data5/2019swh/paint/pentad/pentad_crest_all_"+ipen)
    res1 = True
    res1@gsnDraw      =  False                   ; do not draw the plot
    res1@gsnFrame     =  False
    res1@cnLinesOn    =  False
    res1@mpMinLatF    =  -30
    res1@mpMaxLatF    =  60
    res1@mpMinLonF    =  30
    res1@mpMaxLonF    =  160

    res1@gsnMaximize           = True     ; Make plot fit the frame
    res1@cnFillOn              = False     ; turn on color fill
    ;res1@cnLevelSelectionMode       = "ExplicitLevels" 
    ;res1@cnLevels             = ispan(1000,1600,20)
    res1@cnMissingValPerimOn     = True            ; turn on the missing value perimeter
    res1@cnMissingValPerimColor  = "black"           ; outline the perimeter red
    res1@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fill) 
    res1@cnMissingValFillColor   = "black"          ; color fill missing areas blue
    res1@gsnLeftString           = char_pen(ipen-1)
    res1@tiMainString            = ""
    res1@gsnRightString          = ""
    res1@cnLineLabelsOn          = False
    res1@cnInfoLabelOn      =  False

    plot1 = gsn_csm_contour_map(wks, h(ipen-1,24,:,:), res1)

    res2  = True
    res2@gsnDraw      =  False
    res2@gsnFrame     =  False  
    res2@vcRefAnnoOrthogonalPosF = -1.35             ; move ref vector up
    res2@vcRefMagnitudeF         = 10.0             ; define vector ref mag
    res2@vcRefLengthF            = 0.045            ; define length of vec ref
    res2@vcGlyphStyle            = "CurlyVector"    ; turn on curly vectors
    res2@vcMinDistanceF          = 0.017
    res2@gsnRightString             = ""
    res2@vcMinDistanceF          = 0.022
    res2@vcRefAnnoOn             = False
    plot2 = gsn_csm_vector(wks,u(ipen-1,24,:,:),v(ipen-1,24,:,:),res2)

    res   = True ;画脊线了！！
    res@gsnDraw     =   False
    res@gsnFrame    =   False
    res@cnLevelSelectionMode  =  "ExplicitLevels"
    res@cnLevels    =   (/0/)
    res@cnLineThicknessF  =  5
    res@cnLineColor        =  "red"
    res@gsnLeftString      =  ""
    res@gsnRightString     =  ""
    res@cnInfoLabelOn      =  False
    res@cnRasterMinCellSizeF = 0.01
    res@cnLineLabelsOn     = False
    plot3 = gsn_csm_contour(wks, uu(ipen-1,3,{-10:20},{35:100}), res)
    res@cnLineColor        =  "green"
    plot4 = gsn_csm_contour(wks, uu(ipen-1,7,{-10:28},{37:}), res)
    res@cnLineColor        =  "blue"
    plot5 = gsn_csm_contour(wks, uu(ipen-1,12,{-10:30},{37:}), res)
    res@cnLineColor        =  "brown"
    plot6 = gsn_csm_contour(wks, uu(ipen-1,16,{-10:30},:), res)
    res@cnLineColor        =  "purple"
    plot7 = gsn_csm_contour(wks, uu(ipen-1,24,{-10:30},:), res)

    ;画个图例
    lgres       =  True
    lgres@lgMonoDashIndex   = True
    lgres@lgLineColors  =  (/"red","green","blue","brown","purple"/)
    lgres@lgLineThicknessF  =  5
    lgres@lgItemType         = "Lines"      
    lgres@lgLabelFontHeightF = .08            ; set the legend label font thickness
    lgres@vpWidthF           = 0.15           ; width of legend (NDC)
    lgres@vpHeightF          = 0.1            ; height of legend (NDC)
    lgres@lgPerimColor       = "orange"       ; draw the box perimeter in orange
    lgres@lgPerimThicknessF  = 5.0            ; thicken the box perimeter  
    lbid = gsn_create_legend(wks,5,(/" 925hPa"," 850hPa"," 700hPa"," 500hPa"," 100hPa"/),lgres)         ; create legend
    ;lgres@lgMonoDashIndex   = True


    amres = True
    amres@amParallelPosF   = 0.41		    ; move legend to the right
    amres@amOrthogonalPosF = -0.41             ; move the legend down
    annoid1 = gsn_add_annotation(plot1,lbid,amres)   ; add legend to plot

   ;polyres                   = True
   ;polyres@gsLineColor       = "black"
   ;polyres@gsLineThicknessF  = 5
   ;polyres@gsLineDashPattern = 2
   ;dum = gsn_add_polyline(wks, plot, (/30,150/), (/0,0/), polyres)



    ;overlay(plot1,plot2)
    overlay(plot1,plot3)
    overlay(plot1,plot4)
    overlay(plot1,plot5)
    overlay(plot1,plot6)
    overlay(plot1,plot7)
    

    draw(plot1)
    frame(wks)

end do
end
