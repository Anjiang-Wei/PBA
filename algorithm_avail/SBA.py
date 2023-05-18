import json
import numpy as np
import pprint
from scipy.stats import norm
import random
from random import sample
import math

date="May2"

distributions = {}
def init_model(perc=None):
    random.seed(123)
    with open("../model/retention1s.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(',')
            tmin, tmax, distr = int(tokens[0]), int(tokens[1]), list(map(int, tokens[2:]))
            if perc is not None:
                distr = sorted(sample(distr, int(perc * len(distr))) * math.ceil(1/perc))
            distributions[(tmin, tmax)] = distr
    # print(distributions)


def level_inference(BER):
    levels = []
    for tmin in range(0, 60):
        tmax = tmin + 4
        RelaxDistr = distributions[(tmin, tmax)]
        Rlow, Rhigh = getReadRange(RelaxDistr, BER)
        # assert Rlow <= tmin and tmax <= Rhigh, (Rlow, Rhigh, tmin, tmax)
        if len(levels) == 0:
            levels.append([Rlow, Rhigh, tmin, tmax])
        else:
            # current level's Rlow does not overlap with prior level's Rhigh
            # current level's tmin (write ranges) does not overlap with prior level's tmax
            if Rlow >= levels[-1][1] and tmin >= levels[-1][3]:
                levels.append([Rlow, Rhigh, tmin, tmax])
    levels = refine(levels)
    return levels

def getReadRange(distr, number_of_sigma):
    '''
    Goal: get the read range based on the specified sigma

    distr: the resistance distribution
    number_of_sigma: the SBA technique's input, e.g., 3.
    3 simga is the reported number used in the paper: 
    - Resistive RAM With Multiple Bits Per Cell: Array-Level Demonstration of 3 Bits Per Cell

    API reference:
    https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.norm.html
    '''
    # here we get the read range based on the specified sigma
    sigma = np.std(distr)
    mean = np.mean(distr)
    # Get percentiles using Cumulative Distribution Function (cdf) for normal distribution
    # E.g., norm.cdf(-1, loc=0, scale=1) = 15.87%
    # E.g., normal.cdf(1, loc=0, scale=1) = 84.13%
    percentile1 = norm.cdf(-number_of_sigma, loc=0, scale=1)
    percentile2 = norm.cdf(number_of_sigma, loc=0, scale=1)
    # Given the percentile, and the distribution of write, get the read regions
    read_low = norm.ppf(percentile1, loc=mean, scale=sigma)
    read_high = norm.ppf(percentile2, loc=mean, scale=sigma)
    return read_low, read_high + 1

def refine(level_alloc):
    '''
    Make the level boundaries integer (because ppf may return non-integer),
    and also make starting and ending levels correct
    '''
    #print("before refine", level_alloc)
    level_alloc[0][1] = int(level_alloc[0][1])
    for i in range(1, len(level_alloc)):
        assert level_alloc[i - 1][1] <= level_alloc[i][0] 
        level_alloc[i][0] = int(level_alloc[i][0])
        level_alloc[i][1] = int(level_alloc[i][1])
    level_alloc[0][0] = 0
    level_alloc[len(level_alloc)-1][1] = 64
    return level_alloc

def minimal_BER(sigma_start, sigma_end, sigma_delta):
    res = {}
    while sigma_start <= sigma_end:
        levels = level_inference(sigma_start)
        num_level = len(levels)
        # print(f"Solved for {num_level}")
        if num_level not in res.keys():
            res[num_level] = levels
        sigma_start += sigma_delta
    return res

def read_from_json(filename):
    return json.load(open(filename))

def write_to_json(data, filename):
    json.dump(data, open(filename, "w"), indent=1)

def dump_to_json(level_alloc):
    if len(level_alloc) == 16:
        bits_per_cell = 4
    elif len(level_alloc) == 8:
        bits_per_cell = 3
    elif len(level_alloc) == 4:
        bits_per_cell = 2
    print(len(level_alloc), level_alloc)
    bpc = read_from_json(f"../settings/{bits_per_cell}bpc.json")
    for i in range(0, len(level_alloc)):
        # [Rlow, Rhigh, tmin, tmax]
        bpc['level_settings'][i]["adc_upper_read_ref_lvl"] = level_alloc[i][1]
        bpc['level_settings'][i]["adc_lower_write_ref_lvl"] = level_alloc[i][2]
        bpc['level_settings'][i]["adc_upper_write_ref_lvl"] = level_alloc[i][3]
    write_to_json(bpc, f"../settings/{bits_per_cell}bpc_SBA_{date}.json")


if __name__ == "__main__":
    init_model()
    res = minimal_BER(0.5, 7, 0.1)
    dump_to_json(res[4])
    dump_to_json(res[8])
    # dump_to_json(res[16])
