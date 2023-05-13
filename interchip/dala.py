import json
import pprint

date="May2"

DEBUG = False

distributions = {}
def init_model():
    with open("../model/retention1s.csv", "r") as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(',')
            tmin, tmax, distr = int(tokens[0]), int(tokens[1]), list(map(int, tokens[2:]))
            distributions[(tmin, tmax)] = distr
    # print(distributions)


def level_inference(BER):
    if DEBUG:
        print(BER, "Started")
    levels = []
    for tmin in range(0, 60):
        tmax = tmin + 4
        RelaxDistr = distributions[(tmin, tmax)]
        if DEBUG:
            print(len(RelaxDistr),int(BER * len(RelaxDistr) / 2))
        Rlow, Rhigh = getReadRange(RelaxDistr, BER)
        # assert Rlow <= tmin and tmax <= Rhigh, (Rlow, Rhigh, tmin, tmax)
        levels.append([Rlow, Rhigh, tmin, tmax])
    return longest_non_overlap(levels)

def longest_non_overlap(levels):
    # this is a greedy algorithm
    # levels is a list of levels, each level is a list of [Rlow, Rhigh, tmin, tmax]
    res = []
    # first sort by Rhigh
    sorted_levels = sorted(levels, key=lambda x: x[1])
    res.append(sorted_levels[0])
    cur = sorted_levels[0]
    for i in range(1, len(sorted_levels)):
        nxt = sorted_levels[i]
        # the next level's Rlow does not overlap with the current level's Rhigh
        # the next level's tmin (write ranges) does not overlap with current level's tmax
        if nxt[0] >= cur[1] and nxt[2] >= cur[3]:
            res.append(nxt)
            cur = nxt
    return res


def getReadRange(vals, BER):
    # The read range [Rmin, Rmax) -- any point within [Rmin, Rmax) are within this level
    num_discard = int(BER * len(vals) / 2)
    return vals[num_discard], vals[-num_discard] + 1

def refine(level_alloc):
    '''
    close the gap between adjacent read ranges
    Example: list of [Rlow, Rhigh, tmin, tmax]
        [2, 14, 0, 4], [16, 28, 16, 20], [32, 44, 33, 37], [48, 56, 46, 50]
    --> [2, 15, 0, 4], [15, 30, 16, 20], [30, 46, 33, 37], [46, 56, 46, 50]
    --> [0, ...                                               , 63, ...  ]
    '''
    # print("before refine", level_alloc)
    for i in range(1, len(level_alloc)):
        assert level_alloc[i - 1][1] <= level_alloc[i][0] 
        merge = int((level_alloc[i - 1][1] + level_alloc[i][0]) / 2)
        level_alloc[i - 1][1] = merge
        level_alloc[i][0] = merge
    level_alloc[0][0] = 0
    level_alloc[len(level_alloc)-1][1] = 64
    return level_alloc

def half(level_alloc):
    assert len(level_alloc) % 2 == 0
    res = []
    '''
    [Rlow_i, Rhigh_i, tmin_i, tmax_i], [Rlow_{i+1}, Rhigh_{i+1}, tmin_{i+1}, tmax_{i+1}]
    -->
    [Rlow_i, Rhigh_{i+1}, (tmin_i+tmin_{i+1} ) / 2, (tmax_i+tmax_{i+1} ) / 2] 
    '''
    for i in range(0, int(len(level_alloc) / 2)):
        res.append([level_alloc[i*2][0], level_alloc[i*2+1][1],
                    int((level_alloc[i*2][2] + level_alloc[i*2+1][2]) / 2),
                    int((level_alloc[i*2][3] + level_alloc[i*2+1][3]) / 2)])
    assert len(res) == len(level_alloc) / 2
    return res



def minimal_BER(specified_levels, eps, low_BER = 0, high_BER = 1, double=False):
    # rationale for double: for 4 levels with insufficient data to characterize the error
    #   we need to allocate 8 levels then half the levels
    if double:
        specified_levels = specified_levels * 2
    while high_BER - low_BER > eps:
        cur_BER = (low_BER + high_BER) / 2
        cur_levels = level_inference(cur_BER)
        print(len(cur_levels), cur_BER)
        if len(cur_levels) < specified_levels: # the precision requirement is too strict to be met
            low_BER = cur_BER # make next BER bigger
        elif len(cur_levels) > specified_levels:
            high_BER = cur_BER
        else:
            high_BER = cur_BER
            best_level, best_BER = cur_levels, cur_BER
    if double:
        best_level = half(best_level)
    refined = refine(best_level)
    print(refined, best_BER)
    assert len(refined) == specified_levels / 2 if double else specified_levels
    return refined

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
    bpc = read_from_json(f"../settings/{bits_per_cell}bpc.json")
    for i in range(0, len(level_alloc)):
        # [Rlow, Rhigh, tmin, tmax]
        bpc['level_settings'][i]["adc_upper_read_ref_lvl"] = level_alloc[i][1]
        bpc['level_settings'][i]["adc_lower_write_ref_lvl"] = level_alloc[i][2]
        bpc['level_settings'][i]["adc_upper_write_ref_lvl"] = level_alloc[i][3]
    write_to_json(bpc, f"../settings/{bits_per_cell}bpc_dala_{date}.json")


if __name__ == "__main__":
    init_model()
    dump_to_json(minimal_BER(4, 1e-3, 0, 1, True))
    dump_to_json(minimal_BER(8, 1e-3))
    # dump_to_json(minimal_BER(16, 1e-10))
