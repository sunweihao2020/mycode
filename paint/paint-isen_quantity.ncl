;2020/11/23
;merra2等熵面资料
;绘制等熵面上的物理量
;304K 312K 316K 1 3 4
begin
f = addfile("/data5/2019swh/data/isen_quantity_e.nc","r")
f2 = addfile("/data5/2019swh/data/isentropic_theate_data.nc","r")
u   =   f2->uwind
v   =   f2->vwind
;ug  =   f->ug
;vg  =   f->vg
;lev =   f->lev
;lat   = f->lat
h = f->av
h = h*10E+4
;ff = coriolis_param(lat)
;fy = f*lat
;m = ug
;do t = 0,60
;    do lev = 0,8
;        do lon = 0,575
;            m(t,lev,:,lon) = fy-ug(t,lev,:,lon)
;        end do
;    end do
;end do

char_day=(/"D0-15","D0-14","D0-13","D0-12","D0-11","D0-10","D0-9","D0-8","D0-7","D0-6","D0-5","D0-4","D0-3","D0-2","D0-1","D0","D0+1","D0+2","D0+3","D0+4","D0+5","D0+6","D0+7","D0+8","D0+9","D0+10","D0+11","D0+12","D0+13","D0+14","D0+15"/)
levs = (/1,3,4/)
level = (/"304K","312K","316K"/)

do z=0,2
    do day = 15,35
        wks = gsn_open_wks("pdf","/data5/2019swh/paint/day/"+"isen_quantity_e_"+level(z)+"_"+day)
        gsn_define_colormap(wks,"BlueDarkRed18")
        res = True
        res@cnFillOn              = True 
        res@cnLinesOn             = False  
        ;res@gsnDraw               = False
        ;res@gsnFrame              = False
        res@cnLevelSelectionMode  =  "ExplicitLevels"
        ;res@cnLineColor           =  "red"
        res@cnInfoLabelOn         = False
        res@cnLevels             =  ispan(-6, 6, 2) ;(/160,180,200,220,240,260/);(/280,260,240,220,200,180,160/);ispan(-2,36,1)
        res@cnFillColors         = (/6,7,8,9,12,13,14,15/) ;11,10,9,8,6,5,4,3/) 
        res@cnLineThicknessF      = 3
        res@cnLineLabelsOn        = False
        res@gsnLeftString         = char_day(day-15)
        res@gsnRightString        = level(z)
        res@cnMissingValPerimOn     = True            ; turn on the missing value perim
        res@cnMissingValPerimColor  = "black"           ; outline the perimeter red
        res@cnMissingValFillPattern = 0               ; choose fill pattern 0 (solid fi
        res@cnMissingValFillColor   = "gray"          ; color fill missing areas blue

        res@mpMinLatF            =  0 
        res@mpMaxLatF            =  30.
        res@mpMinLonF            =  60.
        res@mpMaxLonF            =  110.

        plot = gsn_csm_contour_map(wks, h(day,levs(z),2:,:), res)
    end do
end do
end