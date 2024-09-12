import time
import itrm

K = 1000
bar = itrm.Progress(K)
for k in range(K):
    time.sleep(0.01)
    bar.update(k)
print("Done")
