from threading import Timer
import numpy as np

def hello():
    print "hello, world"
    t = Timer(30.0, hello)
    t.start()  # after 30 seconds, "hello, world" will be printed

# t = Timer(30.0, hello)
# t.start() # after 30 seconds, "hello, world" will be printed

a = np.array([[1, 2, 6], [3, 4, 7]])

print a[0][-1]
print a[1][-1]

a = np.insert(a, np.shape(a)[1], [11,12], axis=1)

print a
