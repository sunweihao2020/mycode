begin
    f0  =  addfile("/home/sun/mydown/model_input/b1850/tx0.66v1_SCRIP_190314.nc","r")
    imask0  =  f0->grid_imask
    lat0    =  f0->grid_center_lat

    imask1  =  reshape(imask0,(/540,458/))
    lat1    =  reshape(lat0,(/540,458/))

    ;print(imask1(:,0))
    print(lat1(120,:))

end