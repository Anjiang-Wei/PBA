import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get retention data
header = ["addr,time,after_relax,i,after_write,tmin,tmax,timept"]
distributions = {} # (tmin, tmax) --> [after_relax points]
distri_0s = {} # (tmin, tmax) --> [after_write points]

def init_distributions():
    with open("../data/retention1s2.csv", "r") as f:
        lines = f.readlines()
        lines = lines[1:]
        for line in lines:
            tokens = line.split(',')
            addr = int(tokens[0])
            time = float(tokens[1])
            after_relax = int(tokens[2])
            i = int(tokens[3])
            after_write = int(tokens[4])
            tmin = int(tokens[5])
            tmax = int(tokens[6])
            timept = int(tokens[7])
            assert timept == 1
            if (tmin, tmax) not in distributions:
                distributions[(tmin, tmax)] = []
                distri_0s[(tmin, tmax)] = []
            # only use 200 cells' data
            # if len(distributions[(tmin, tmax)]) == 200:
            #     continue
            distributions[(tmin, tmax)].append(after_relax)
            distri_0s[(tmin, tmax)].append(after_write)

def check():
    if len(distributions) != 60:
        print("ERROR:", len(distributions))
    for tmin in range(0, 60):
        tmax = tmin + 4
        distributions[(tmin, tmax)].sort()
        if len(distributions[(tmin, tmax)]) < 200:
            print("ERROR:", tmin, tmax, len(distributions[(tmin, tmax)]))
        distri_0s[(tmin, tmax)].sort()
        if len(distri_0s[(tmin, tmax)]) < 200:
            print("ERROR:", tmin, tmax, len(distri_0s[(tmin, tmax)]))

def dump():
    with open("../model/retention1s2.csv", "w") as f:
        for tmin in range(0, 60):
            tmax = tmin + 4
            f.write(f"{tmin},{tmax},{','.join(map(str, distributions[(tmin, tmax)]))}\n")
    # with open("../model/retention0s.csv", "w") as f:
    #     for tmin in range(0, 60):
    #         tmax = tmin + 4
    #         f.write(f"{tmin},{tmax},{','.join(map(str, distri_0s[(tmin, tmax)]))}\n")

if __name__ == "__main__":
    init_distributions()
    check()
    dump()