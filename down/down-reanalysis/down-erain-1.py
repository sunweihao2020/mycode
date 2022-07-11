from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
    "class": "ei",
    "dataset": "interim",
    "date": "1979-01-01/to/2010-12-31",
    "expver": "1",
    "grid": "1.0/1.0",
    "levtype": "sfc",
    "param": "166.128",
    "step": "0",
    "stream": "oper",
    "time": "00:00:00/06:00:00/12:00:00/18:00:00",
    "type": "an",
    'format': "netcdf",
    "target": "1979-2010_erain_u10.nc",
})