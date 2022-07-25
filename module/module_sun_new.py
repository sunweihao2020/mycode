''''
2022-7-24
This script is new module sun py files
Purpose is to solve some problems in the module_sun.py
'''
def cal_xydistance(lat,lon):
    '''Use lat and lon to calculate distence message'''
    # ---import---
    import numpy as np
    from geopy.distance import distance

    disy = np.array([])
    disx = np.array([])
    for i in range(0, (lat.shape[0]-1)):
        disy = np.append(disy, distance((lat[i], 0), (lat[i + 1], 0)).m)

    for i in range(0, lat.shape[0]):
        disx = np.append(disx, distance((lat[i], lon[0]), (lat[i], lon[1])).m)

    location = np.array([0])
    for dddd in range(0, (lat.shape[0]-1)):
        location = np.append(location, np.sum(disy[:dddd + 1]))

    return disy,disx,location
