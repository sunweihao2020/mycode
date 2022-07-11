#!/usr/bin/env python
import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-complete', {
    'class': 'ea',
    'date': '1985-06-12',
    'expver': '1',
    'levelist': '136/137',
    'levtype': 'ml',
    'param': '235005',
    'step': '1/2/3/4/5/6/7/8/9/10/11/12',
    'stream': 'oper',
    'time': '06:00:00/18:00:00',
    'type': 'fc',
}, 'output')