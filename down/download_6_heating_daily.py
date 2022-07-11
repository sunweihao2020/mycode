#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
import sys
import os
server = ECMWFDataServer()
def down(yyyy):
    server.retrieve({
        "class": "ei",
        "dataset": "interim",
        "date": str(yyyy)+"-03-01/to/"+str(yyyy)+"-05-31",
        "expver": "1",
        "grid": "1.5/1.5",
        "levtype": "sfc",
        "param": "146.128/147.128/169.128/176.128/178.128/179.128",
        "step": "12",
        "stream": "oper",
        "time": "00:00:00/12:00:00",
        "type": "fc",
        "format": "netcdf",
        "target": str(yyyy)+".nc",
    })

for yyyy in range(1980,2018):
    down(yyyy)