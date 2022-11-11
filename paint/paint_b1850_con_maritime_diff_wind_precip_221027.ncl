;2022/10/27
;This code calculate the difference between control and maritime experiment
;paint variables: wind precip
;lev: 850
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/shea_util.ncl"
begin
path_out   =  "/home/sun/data/model_data/climate/"
file_out1  =  "b1850_control_atmospheric_monthly_average_2.nc"
file_out2  =  "b1850_maritime_atmospheric_monthly_average_2.nc"
f0         =  addfile(path_out + file_out1,  "r")
f1         =  addfile(path_out + file_out2,  "r")

; read variable
ctl_u = f0->U(:,{850},:,:)
ctl_v = f0->V(:,{850},:,:)
mar_u = f1->U(:,{850},:,:)
mar_v = f1->V(:,{850},:,:)

ctl_precip  =  f0->PRECT
mar_precip  =  f1->PRECT

; replace nan
ctl_u@_FillValue   =  9999
ctl_v@_FillValue   =  9999
mar_u@_FillValue   =  9999
mar_v@_FillValue   =  9999
if (any(isnan_ieee(ctl_u))) then
replace_ieeenan (ctl_u, ctl_u@_FillValue, 0)
replace_ieeenan (ctl_v, ctl_v@_FillValue, 0)
replace_ieeenan (mar_u, mar_u@_FillValue, 0)
replace_ieeenan (mar_v, mar_v@_FillValue, 0)

end if


char_month=(/"June","JULY","August","November"/)
num_month = (/5,6,7,8/)

lev       = (/6/)
level = (/"850hPa"/)

; calculate difference
diff_u      =  ctl_u
diff_v      =  ctl_v
diff_precip = ctl_precip

diff_u      =   mar_u  -  ctl_u 
diff_v      =   mar_v  -  ctl_v 
diff_precip =   ((mar_precip - ctl_precip)) * 86400000  ; The percentage of changed precipitation

; ---- contour setting -------------
res                       = True

;lines
res@cnFillOn              = True
res@cnFillPalette         = "BlueDarkRed18"
res@cnLineLabelsOn        = False
res@cnLinesOn             = False
res@cnInfoLabelOn         = False 
res@cnLevelSelectionMode  = "ExplicitLevels" 
res@cnLevels              = fspan(-3,3,13)

res@gsnDraw               = False
res@gsnFrame              = False

; map settings
res@mpMinLatF             = -20 
res@mpMaxLatF             =  50.
res@mpMinLonF             =  40.
res@mpMaxLonF             =  280.
res@mpGeophysicalLineThicknessF  = 1

; labelbar
res@lbLabelBarOn          = False

;tick and ticklabel
res@tmYLLabelFontHeightF   =  0.024
res@tmXBLabelFontHeightF  =  0.024

; String
res@gsnRightString        =  "850 hPa"
res@gsnStringFont         =  0.5


; -------  vector settings  ----------
vcres                     =  True

vcres@gsnDraw             =  False
vcres@gsnFrame            =  False

; magnitude for ref
vcres@vcRefMagnitudeF     =  2.5

; vector length
vcres@vcRefLengthF        =  0.05

;vector style
vcres@vcGlyphStyle        = "CurlyVector"
vcres@vcMinDistanceF      = 0.017

; Strings
vcres@gsnLeftString       =  ""
vcres@gsnRightString      =  ""

;vector reference
vcres@vcRefAnnoOrthogonalPosF = -0.3

;stres = True
;stres@gsnDraw    = False
;stres@gsnFrame   = False
;stres@stArrowLengthF     = 0.008  
;stres@stLengthCheckCount = 15
;stres@stArrowStride      = 1
;stres@stMinArrowSpacingF = 0.025
;stres@stLineThicknessF   = 0.7
;;stres@stLevelSpacingF    = 25
;stres@gsnStringFont         = 2
;stres@gsnRightString = " "
;stres@tmYLLabelFontHeightF      = 0.024
;stres@tmXBLabelFontHeightF      = 0.024
;stres@stLineStartStride  = 20                    ; default is 2            
;stres@stStepSizeF        = 0.001                ; default is dynamic
;
;polyres                   = True
;polyres@gsLineColor       = "black"
;polyres@gsLineThicknessF  = 1
;polyres@gsLineDashPattern = 2

; figure setting
plot1 = new(4,graphic)
wks1 = gsn_open_wks("pdf","/home/sun/paint/b1850_exp/difference_in_sensitivity/b1850_diff_monthly_925_circulation_with_prect")


; plot
do day = 0,3
    res@gsnLeftString = char_month(day)
    
    plot1(day) = gsn_csm_contour_map(wks1,diff_precip(num_month(day),:,:),res)

    a = gsn_csm_vector(wks1,diff_u(num_month(day),:,:), diff_v(num_month(day),:,:), vcres)
    
    overlay(plot1(day),a)
    ;print(day)
end do

pnlres = True
;pnlres@gsnPanelMainString = "wind at "+level(ll)+" & divergence"
pnlres@gsnPanelLabelBar  = True
;pnlres@gsnPanelDebug     = True     ; To get information from panel
;pnlres@lbLabelFontHeightF = 0.015
gsn_panel(wks1,plot1,(/2,2/),pnlres)

;frame(wks1)
end