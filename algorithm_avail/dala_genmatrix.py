import dala
import numpy

outfile = "../ember_avail/"
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

def simulate_all_levels(dala_allocs, percnum):
    for i in [8]:
        P = simulate_error(dala_allocs[i])
        dump_matrix(P, outfile + str(int(percnum)) + "/" + whos)

def dump_matrix(matrix, hint):
    num_level = len(matrix)
    with open(hint + str(num_level), "w") as fout:
        to_write = []
        for i in range(len(matrix)):
            to_write.append(",".join(map(str, matrix[i])) + "\n")
        fout.writelines(to_write)

def gen(perc):
    print(perc)
    dala.distributions = {}
    dala.init_model(perc)
    dala_allocs = get_dala()
    dala.init_model()
    simulate_all_levels(dala_allocs,100*perc)

if __name__ == "__main__":
    # gen(0.1)
    gen(0.25)
    gen(0.5)
    gen(0.75)
    gen(0.9)
    # gen(1.0)
