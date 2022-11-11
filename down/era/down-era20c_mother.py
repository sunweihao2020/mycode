#!/usr/bin/env python
from ecmwfapi import ECMWFDataServer
server = ECMWFDataServer()
server.retrieve({
    "class": "e2",
    "dataset": "era20c",
    "date": "19000101/19000201/19000301/19000401/19000501/19000601/19000701/19000801/19000901/19001001/19001101/19001201",
    "expver": "1",
    "levelist": "500/850/950",
    "levtype": "pl",
    "param": "130.128/131.128/132.128",
    "stream": "moda",
    "type": "an",
    "target": "output",
})