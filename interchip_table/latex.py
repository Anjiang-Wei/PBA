import pprint

same = [
    "../ember_capacity/", # dataset1, eval on chip1
    "../ember_capacity2/", # dataset2, eval on chip2
]
other = [
    "../intercapacity2/", # dataset2, eval on chip1
    "../intercapacity/", # dataset1, eval on chip2
]
equal = [
    "../bothcapacity/", # both dataset, eval on chip1
    "../bothcapacity2/", # both dataset, eval on chip2
]
biased = [
    "../domin_capacity2/", # most dataset2, eval on chip1
    "../domin_capacity/", # most dataset1, eval on chip2
]

sba_res = {
    # CHIP1: 3bpc BER, overhead;  CHIP2: 3bpc BER, overhead
    "same": [],
    "other": [],
    "equal": [],
    "biased": [], 
}

ours_res = {
    # CHIP1: 3bpc BER, overhead;  CHIP2: 3bpc BER, overhead
    "same": [],
    "other": [],
    "equal": [],
    "biased": [],
}

def get_ber(path, level_num=8):
    ours8 = -1
    SBA8 = -1
    with open(path + "log_trans") as fin:
        lines = fin.readlines()
        for line in lines:
            # 'ours8' : 0.003795615468409586,
            if "ours" + str(level_num) in line:
                ours8 = float(line.split(" : ")[-1].split(",")[0])
            if "SBA" + str(level_num) in line:
                SBA8 = float(line.split(" : ")[-1].split(",")[0])
    return ours8, SBA8

def get_ecc(path, level_num=8):
    ours8 = -1
    SBA8 = -1
    start = False
    with open(path + "log_ecc") as fin:
        lines = fin.readlines()
        for line in lines:
            # 'ours8': ['RS', 1.091127098321343, 455, 417, 39, 9, 3.1108264639185265e-15]}
            if "No bigger than 4096" in line:
                start = True
            if "No bigger than 8192" in line:
                start = False
            if start:
                if "ours" + str(level_num) in line:
                    ours8 = float(line.split(" : ")[-1].split(",")[1])
                if "SBA" + str(level_num) in line:
                    SBA8 = float(line.split(" : ")[-1].split(",")[1])
    return ours8, SBA8


def filldata(dataset_str, path):
    chipA_ber_ours, chipA_ber_SBA = get_ber(path[0])
    chipA_ecc_ours, chipA_ecc_SBA = get_ecc(path[0])
    chipB_ber_ours, chipB_ber_SBA = get_ber(path[1])
    chipB_ecc_ours, chipB_ecc_SBA = get_ecc(path[1])
    ours_res[dataset_str] = [[chipA_ber_ours, chipA_ecc_ours], 
                            [chipB_ber_ours, chipB_ecc_ours]]
    sba_res[dataset_str] = [[chipA_ber_SBA, chipA_ecc_SBA],
                            [chipB_ber_SBA, chipB_ecc_SBA]]

def fill_dict():
    filldata("same", same)
    filldata("other", other)
    filldata("equal", equal)
    filldata("biased", biased)


if __name__ == "__main__":
    fill_dict()
    pprint.pprint(ours_res)
    pprint.pprint(sba_res)