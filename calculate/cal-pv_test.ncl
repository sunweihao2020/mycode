;2020/12/24
;用ncl的差分计算位涡测试
begin
f = addfile("model_theta_19800301.nc","r")
u = f->uwind
v = f->vwind
theta = f->theta
lat = f->lat
p = f->PL
dim        := dimsizes(p)
gradLatLon := grad_latlon_cfd(theta, theta&lat, theta&lon, True, False)

g           = 9.8  ;m/s2
pi          = 3.14159
OMEGA       = todouble(7.292*10^(-5)) ;地球自转角速度

theta_y    := gradLatLon[0]    ;double
theta_x    := gradLatLon[1]    ;float
theta_p   := center_finite_diff_n(theta, p, False, 0 , 1)          ;float  
v_p        := center_finite_diff_n(v, p, False, 0 , 1)               ;float
u_p        := center_finite_diff_n(u, p, False, 0 , 1)                ;float
gradLatLon := grad_latlon_cfd(v, v&lat, v&lon, True, False)           
v_x        := gradLatLon[1] 
gradLatLon := grad_latlon_cfd(u, u&lat, u&lon, True, False)
u_y        := gradLatLon[0] 
ff         := 2*OMEGA*conform_dims(dim, sin(lat), 2)

P         := g*(v_p*theta_x - u_p*theta_y) -  g*((v_x -  u_y + ff)*theta_p)  