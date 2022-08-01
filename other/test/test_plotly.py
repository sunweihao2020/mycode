import plotly.figure_factory as ff

import numpy as np

x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 50)
Y, X = np.meshgrid(x, y)
u = -1 - X**2 + Y
v = 1 + X - Y**2

# Create streamline figure
fig = ff.create_streamline(x, y, u, v, arrow_scale=.1)