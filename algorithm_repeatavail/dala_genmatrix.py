import dala
import numpy

outfile = "../ember_repeatavail/"
whos = "ours"

def decide_end_level(point, level_alloc):
    for i in range(len(level_alloc)):
        rmin, rmax, wmin, wmax = level_alloc[i]    
        if point >= rmin and point < rmax:
            return i
    if point == 64: # last level
        return len(level_alloc)-1
    assert False, point

def simulate_error(level_alloc):
    num_levels = len(level_alloc)
    P = numpy.zeros((num_levels, num_levels))
    num_points = 0
    for i in range(len(level_alloc)):
        rmin, rmax, wmin, wmax = level_alloc[i]    
        d1s = dala.distributions[(wmin, wmax)]
        for point in d1s:
            end_level = decide_end_level(point, level_alloc)
            P[end_level][i] += 1
        for j in range(0, len(level_alloc)):
            P[j][i] = P[j][i] / len(d1s)
        num_points += len(d1s)
    return P

def get_dala():
    res = {}
    for i in [8]:
        res[i] = dala.minimal_BER(i, 1e-3)
    print(res)
    return res

def simulate_all_levels(dala_allocs, percnum, idx):
    for i in [8]:
        P = simulate_error(dala_allocs[i])
        dump_matrix(P, outfile + str(int(percnum)) + "/" + whos, idx)

def dump_matrix(matrix, hint, idx):
    num_level = len(matrix)
    assert num_level == 8, num_level
    with open(hint + str(idx), "w") as fout:
        to_write = []
        for i in range(len(matrix)):
            to_write.append(",".join(map(str, matrix[i])) + "\n")
        fout.writelines(to_write)

def gen(perc,init_seed):
    print(perc, init_seed)
    dala.distributions = {}
    for i in range(0, 10):
        print(i)
        try:
            dala.init_model(perc, init_seed+i)
            dala_allocs = get_dala()
            dala.init_model()
            simulate_all_levels(dala_allocs,int(100*perc),i)
        except:
            dala.init_model(perc, init_seed)
            dala_allocs = get_dala()
            dala.init_model()
            simulate_all_levels(dala_allocs,int(100*perc),i)

if __name__ == "__main__":
    # gen(0.1)
    start_seed=145
    gen(0.25,start_seed)
    gen(0.5,start_seed)
    gen(0.75,start_seed)
    gen(0.9,start_seed)
    gen(1.0,start_seed)
