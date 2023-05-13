

def getmodel(filename):
    distributions = {}
    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            tokens = line.split(',')
            tmin, tmax, distr = int(tokens[0]), int(tokens[1]), list(map(int, tokens[2:]))
            distributions[(tmin, tmax)] = distr
    return distributions

def merged(d1, d2):
    assert d1.keys() == d2.keys()
    res = {}
    for k in d1.keys():
        res[k] = d1[k] + d2[k]
    return res

def dump_model(distributions, filename):
    with open(filename, "w") as f:
        for tmin in range(0, 60):
            tmax = tmin + 4
            f.write(f"{tmin},{tmax},{','.join(map(str, distributions[(tmin, tmax)]))}\n")

def merge(f1, f2, fout):
    d1 = getmodel(f1)
    d2 = getmodel(f2)
    d3 = merged(d1, d2)
    dump_model(d3, fout)

if __name__ == "__main__":
    merge("retention1s.csv", "retention1s2.csv", "retention1smerge.csv")