from scipy.special import comb
import pickle
import math
import numpy as np
import pprint
import os

db = {}
# (base, n, k) --> [d, "tag"]
# overhead: n / k

def P_cw(N, E, RBER, spec_ber):
    '''
    N: block length; the number of cells for output [length of codeword]
    E: the number of errors that can be corrected
    RBER: Raw BER; the probability of level drift; worst case analysis
    # actually RBER depends on q
    '''
    res = 0
    for i in range(E+1, N+1):
        res += comb(N, i) * pow(RBER, i) * pow(1-RBER, N-i)
        if res > spec_ber:
            return 1
    return res


def RS():
    '''
    <n, k, n-k+1>_[p^m]: n <= p^m, p = 2
    '''
    res = {}
    p = 2
    for base in range(1, 11):
        for n in range(2, (p**base) + 1):
            for k in range(1, n):
                d = n - k + 1
                new_key = (base, n, k)
                res[new_key] = [d, "RS"]
    # print(res)
    return res

def Hamming():
    '''
    <2^r - 1, 2^r - r - 1, 3> (r >= 2)
    '''
    res = {}
    for r in range(2, 11):
        n = (2 ** r) - 1
        k = (2 ** r) - r - 1
        d = 3
        new_key = (1, n, k)
        res[new_key] = [d, "Hamming"]
    # pprint.pprint(res)
    return res

def BCH():
    '''
    https://web.ntpu.edu.tw/~yshan/BCH_code.pdf --> BCH.txt
    d = 2t + 1
    '''
    res = {}
    filename = "BCH.txt"
    if "ecc" not in os.getcwd():
        filename = "../ecc/BCH.txt"
    with open(filename, "r") as fin:
        lines = fin.readlines()[1:]
        for line in lines:
            n, k, t = map(int, line.split(","))
            d = 2 * t + 1
            new_key = (1, n, k)
            res[new_key] = [d, "BCH"]
    # print(res)
    return res

def merge(dict1, dict2):
    # merge two dicts and reserve max
    res = dict2.copy()
    for key in dict1.keys():
        if key not in res.keys():
            res[key] = dict1[key]
        else:
            res[key] = max(dict1[key], dict2[key])
    return res

def mergeall(dicts):
    assert len(dicts) > 0
    if len(dicts) == 1:
        return dicts[0]
    if len(dicts) == 2:
        return merge(dicts[0], dicts[1])
    res = merge(dicts[0], dicts[1])
    for edict in dicts[2:]:
        res = merge(res, edict)
    return res

def allcode():
    return mergeall([RS(), Hamming(), BCH()])


def bestcode(codes, spec_ber, raw_ber, maxk, maxn):
    best_overhead = 10
    best_config = ["None", 1e10, -1, -1, -1, -1, -1]
    for codekey in codes.keys():
        base, n, k = codekey
        d, tag = codes[codekey]
        if n / k < best_overhead and (k * base <= maxk and n * base <= maxn):
            uber = P_cw(n, int((d-1)/2), raw_ber, spec_ber)
            if uber <= spec_ber:
                best_overhead = n / k
                best_config = [tag, best_overhead, n, k, d, base, uber]
    return best_config

def bestcode_dict(codes, spec_ber, raw_ber_dict, maxk, maxn):
    res = {}
    for key in raw_ber_dict.keys():
        val = bestcode(codes, spec_ber, raw_ber_dict[key], maxk, maxn)
        res[key] = val
    return res

def report_improve(ecc_res):
    res = ecc_res
    our4 = ecc_res['ours4'][1] - 1
    sba4 = ecc_res['SBA4'][1] - 1
    res['Overhead_Ratio_4'] = sba4 / our4
    res['Reduction_in_Overhead_Ratio_4'] = (sba4 - our4) / sba4
    our8 = ecc_res['ours8'][1] - 1
    sba8 = ecc_res['SBA8'][1] - 1
    res['Overhead_Ratio_8'] = sba8 / our8
    res['Reduction_in_Overhead_Ratio_8'] = (sba8 - our8) / sba8

    pprint.pprint(res)

# obtained from trans.py
raw_ber = {\
'ours4' : 0.0,
'ours8' : 0.004553036492374728,
'SBA4' : 0.0009191176470588235,
'SBA8' : 0.006246595860566449,
}
error_spec = 1e-14

if __name__ == "__main__":
    report_improve(bestcode_dict(allcode(), error_spec, raw_ber, 1e10, 1e10))
    print("Add Constraints")
    for i in range(7, 14):
        print("No bigger than", 2**i)
        report_improve(bestcode_dict(allcode(), error_spec, raw_ber, 2**i, 2**i))