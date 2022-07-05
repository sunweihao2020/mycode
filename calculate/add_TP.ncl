;***************11
undef("overlay_x_longitude")
function overlay_x_longitude(wks,plot,latlon,color)
begin

f=addfile("/data5/2019swh/data/orography_etopo_to_surface_pressure.nc","r")
pres=f->ps
lat=f->lat
lon=f->lon

 ydim = dimsizes(pres)
;x-axis is longitude
 yp  = new((/ydim(0),2*ydim(1)/),"double")
 xp  = new((/2*ydim(1)/),"double")
 do k = 0,ydim(1)-1
 yp(:,k) = pres(:,k)
 yp(:,2*ydim(1)-1-k) = 1000
 xp(k) =  lon(k)
 xp(2*ydim(1)-1-k) = lon(k)
 end do

  gsres  = True
  gsres@gsFillColor= color
  gsres@gsLineColor =color
dum =gsn_add_polygon(wks,plot,xp,yp({latlon},:),gsres)
return(dum)
end




undef("overlay_x_latitude")
function overlay_x_latitude(wks,plot,latlon,color)
begin

f=addfile("/data5/2019swh/data/orography_etopo_to_surface_pressure.nc","r")
pres=f->ps
lat=f->lat
lon=f->lon
;x-axis is latitude
 ydim = dimsizes(pres)
 yp1  = new((/2*ydim(0),ydim(1)/),"double")
 xp1  = new((/2*ydim(0)/),"double")
 do k = 0,ydim(0)-1
 yp1(k,:) = pres(k,:)
 yp1(2*ydim(0)-1-k,:) = 1000
 xp1(k) =  lat(k)
 xp1(2*ydim(0)-1-k) = lat(k)
 end do
 delete(ydim)

  gsres  = True
  gsres@gsFillColor= color
  gsres@gsLineColor =color


dum =gsn_add_polygon(wks,plot,xp1,yp1(:,{latlon}),gsres)
return(dum)
end

