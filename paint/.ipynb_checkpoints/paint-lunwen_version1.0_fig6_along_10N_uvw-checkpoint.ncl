;2021/12/21
;本代码绘制论文中的fig6
;包含要素为沿10N的v等值线图、u-w的矢量图
begin

path1 =   "/home/sun/qomo-data/"
path2 =  "/home/sun/paint/lunwen/version1.0/"

f    =   addfile(path1+"composite3.nc","r")
v    =   f->vwind(:,:,{10:15},{40:120})
u    =   f->uwind(:,:,{10:15},{40:120})
w    =   f->OMEGA(:,:,{10:15},{40:120})

w    =   w*-60

avg_v  =  dim_avg_n_Wrap(v, 2)
avg_u  =  dim_avg_n_Wrap(v, 2)
avg_w  =  dim_avg_n_Wrap(w, 2)

char_day=(/"D0-6","D0-3","D0","D0+3"/)

res                      = True        

res@cnLineLabelsOn       = False
res@cnLevelSelectionMode = "ExplicitLevels"
res@cnLevelSpacingF      = ispan(-8,8,1)                            
res@cnFillOn             = True          
res@cnFillPalette        = "BlueRed"     
res@cnInfoLabelOn        = False 

res@lbLabelBarOn         =     False

res@gsnContourZeroLineThicknessF = 1.5
res@gsnContourNegLineDashPattern = 1
res@gsnRightString       = " "

res@tmXBMode             = "Explicit"
res@tmXBValues           = ispan(40,120,10)
res@tmXBLabels           = ispan(40,120,10)
;res@tmXBMinorValues      = ispan(40,120,1)
res@tmXBLabelFontHeightF = 0.038

res@cnMissingValPerimOn     = True        
res@cnMissingValPerimColor  = "black"     
res@cnMissingValFillPattern = 0           
res@cnMissingValFillColor   = "black"   

;-----矢量------
res                             = True

res@gsnDraw                     = False 
res@gsnFrame                    = False 

res@vcRefAnnoOn                 = True
res@vcRefLengthF                = 0.04
res@vcRefAnnoOrthogonalPosF     = -1.1   
res@vcRefAnnoString1On          = False       
res@vcRefAnnoString2On          = True 
res@vcRefAnnoString2            = "5 m/s"
res@vcRefMagnitudeF             =   5              ; define vector ref mag
res@vcRefAnnoFontHeightF        = 0.017
res@vcRefAnnoPerimOn            = True

res@vcMinDistanceF              = 0.03
res@vcGlyphStyle                = "CurlyVector"
res@vcLineArrowThicknessF       = 1
res@vcLineArrowHeadMaxSizeF     = 0.025
res@vcLineArrowHeadMinSizeF     = 0.004
res@vcMinFracLengthF            = 0.2

plot  = new(4,graphic)
dum   = new(4,graphic)
wks   = gsn_open_wks ("pdf", path2+"lunwen_version1.0_fig6_along_10_uvw" )

day  =  (/24,27,30,33/)  
do dd = 0,3
res@gsnLeftString = char_day(dd)
plot(dd) = gsn_csm_pres_hgt_vector(wks,avg_v(day(dd),{1000:200},:),avg_u(day(dd),{1000:200},:),avg_w(day(dd),{1000:200},:),res )  
end do

pnlres = True
pnlres@lgPerimOn             = False
pnlres@lgAutoManage          = False
pnlres@lgLineLabelStrings    = (/"",""/)
pnlres@gsnPanelLabelBar  = True
pnlres@pmLabelBarWidthF  = 0.55
pnlres@lbLabelFontHeightF = 0.012
pnlres@gsnPanelDebug     = True  
pnlres@gsnPanelMainString = "vwind(10N)"
gsn_panel(wks,plot,(/1,4/),pnlres)
end