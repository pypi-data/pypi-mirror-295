import numpy as np
import itrm

t = np.linspace(0, 2*np.pi, 1000)
x = np.cos(t)
y = np.sin(t)

xd = [-2, 2, 2, -2]
yd = [-2, -2, 2, 2]

#itrm.CONFIG.ar = 3
itrm.plot([x, xd], [y, yd], ea=True)
