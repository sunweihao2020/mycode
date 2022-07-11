#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
    'class': 'ea',
    'date': '1985-05-05',
    'expver': '1',
    'levelist': '5',
    'levtype': 'ml',
    'param': '152',
    'step': '3',
    'stream': 'oper',
    'time': '06:00:00',
    'type': 'fc',
}, 'output')