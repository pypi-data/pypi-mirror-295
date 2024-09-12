import numpy as np
import itrm

x = np.random.rand(5, 3)
names = ['apples', 'bananas', 'pears', 'oranges', 'grapes']
headers = ['Set 1', 'Set 2', 'Set 3']
itrm.table(x, left=names, head=headers)
