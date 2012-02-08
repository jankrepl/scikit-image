import numpy as np
from numpy.testing import *

import time
import random
import skimage.graph.heap as heap

def test_heap():
    _test_heap(100000, True)
    _test_heap(100000, False)

def _test_heap(n, fast_update):
    # generate random numbers with duplicates
    random.seed(0)
    a = [random.uniform(1.0,100.0) for i in range(n//2)]
    a = a+a
    
    t0 = time.clock()
    
    # insert in heap with random removals
    if fast_update:
        h = heap.FastUpdateBinaryHeap(128, n)
    else:
        h = heap.BinaryHeap(128)
    for i in range(len(a)):
        h.push(a[i], i)
        if a[i] < 25:
          # double-push same ref sometimes to test fast update codepaths
          h.push(2*a[i], i)
        if 25 < a[i] < 50:
          # pop some to test random removal
          h.pop()
    
    # pop from heap
    b = []
    while True:
        try:
            b.append(h.pop()[0])
        except IndexError:
            break
    
    t1 = time.clock()
    
    # verify
    for i in range(1,len(b)):
        assert(b[i] >= b[i-1])
    
    return t1-t0

if __name__ == "__main__":
    run_module_suite()