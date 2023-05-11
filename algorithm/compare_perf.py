import dala
import SBA
import time
# import matplotlib.pyplot as plt

def simlute_error(level_alloc):
    count = 0
    total = 0
    for item in level_alloc:
        rmin, rmax, wmin, wmax = item    
        d1s = dala.distributions[(wmin, wmax)]
        for point in d1s:
            if rmin <= point and point < rmax:
                count += 1
            total += 1
    return count / total, total

def compare(dala, sba):
    assert len(dala) == len(sba)
    error1, total = simlute_error(dala)
    error2, _ = simlute_error(sba)
    to_print = [len(dala),error1, error2, total]
    print(",".join(map(str, to_print)))

def get_dala():
    res = {}
    start = time.time()
    for i in range(4, 9):
        if i <= 5:
            res[i] = dala.minimal_BER(i, 1e-3, 0, 1, True)
        else:
            res[i] = dala.minimal_BER(i, 1e-3)
    end = time.time()
    for i in range(4, 9):
        assert(len(res[i]) == i)
    print("DALA", res, end-start)
    return res, end-start

def get_sba():
    SBA.init_model()
    start = time.time()
    res = SBA.minimal_BER(1.8, 6, 0.1)
    end = time.time()
    for i in range(4, 9):
        assert(len(res[i]) == i)
    print("SBA", res, end-start)
    return res, end-start

if __name__ == "__main__":
    dala.init_model()
    dala_alloc, dala_perf = get_dala()
    sba_alloc, sba_perf = get_sba()
    print("levels,dala,sba,total")
    for i in range(4, 9):
        compare(dala_alloc[i], sba_alloc[i])
    print(",".join(map(str, ["performance", dala_perf, sba_perf])))