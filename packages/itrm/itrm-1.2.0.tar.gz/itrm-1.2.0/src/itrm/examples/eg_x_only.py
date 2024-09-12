import numpy as np
import itrm

# Constants
K = 100000

x = np.linspace(0, 1, K)
y = np.cos(2*np.pi*2*x)

itrm.iplot(y)
