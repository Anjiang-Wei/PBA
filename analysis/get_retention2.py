import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Get retention data
names = ["addr", "time", "lvl"]
data = pd.read_csv("../data/retention2.csv.gz", delimiter='\t', names=names)
data["lvl"] = data["lvl"].str.strip('[]').str.split(', ')
data = data.explode("lvl", ignore_index=True)
data["lvl"] = pd.to_numeric(data["lvl"])
data["i"] = data.index % 16
data["time"] -= data.groupby(["addr","i"])["time"].transform("first") 
data["lvli"] = data.groupby(["addr","i"])["lvl"].transform("first")
data["tmin"] = data["addr"] % 60
data["tmax"] = data["addr"] % 60 + 4

# data.to_csv("retention.csv", header=False, index=False)

tdata = []
# times = [0, 0.1, 1, 10, 100, 1000, 10000]
times = [1]
for time in times:
    idx = (data["time"] - time).abs().groupby([data["addr"], data["i"]]).idxmin()
    d = data[data.index.isin(idx)]
    # print(len(d))
    d = d[(d["time"] <= time*1.2) & (d["time"] >= time*0.8)]
    print(len(d))
    d["timept"] = time
    tdata.append(d)
tdata = pd.concat(tdata)
tdata.to_csv("../data/retention1s2.csv", header=["addr","time","after_relax","i","after_write","tmin","tmax","timept"], index=False)