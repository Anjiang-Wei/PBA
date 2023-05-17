import pprint

originalchip = "../ori_capacity/"
emberchip = "../ember_capacity/"
emberchiptwo = "../ember_capacity2/"


sba_res = {
    # 2bpc BER, overhead; 3bpc BER, overhead
    "originalchip": [],
    "emberchip": [],
    "emberchiptwo": [],
}

ours_res = {
    # 2bpc BER, overhead; 3bpc BER, overhead
    "originalchip": [],
    "emberchip": [],
    "emberchiptwo": [],
}

delta_ber = {
    # 2bpc absolute delta (ours_ber - sba_ber), relative (ours_ber-sba_ber)/sba_ber; 3bpc ...
    "originalchip": [],
    "emberchip": [],
    "emberchiptwo": [],
}

delta_ecc = {
    # 2bpc absolute delta (ours_ecc - sba_ecc), relative (ours_ecc-sba_ecc)/sba_ecc; 3bpc ...
    "originalchip": [],
    "emberchip": [],
    "emberchiptwo": [],
}

def get_ber(path, level_num):
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

def get_ecc(path, level_num):
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

def compute_abs_rel(x, y):
    # x is ours, y is SBA
    return [x - y, ((x - y) / y if y != 0 else "N/A")]

def list_to_percent(lst_of_lst):
    res = []
    for i in range(len(lst_of_lst)):
        res.append([])
        for j in range(len(lst_of_lst[i])):
            res[i].append(to_percent(lst_of_lst[i][j]))
    return res

def filldata(dataset_str, path):
    chip_ber_ours_4, chip_ber_SBA_4 = get_ber(path, 4)
    chip_ber_ours_8, chip_ber_SBA_8 = get_ber(path, 8)
    chip_ecc_ours_4, chip_ecc_SBA_4 = get_ecc(path, 4)
    chip_ecc_ours_8, chip_ecc_SBA_8 = get_ecc(path, 8)
    if chip_ber_ours_4 == 0:
        chip_ecc_ours_4 = 1
    if chip_ber_SBA_4 == 0:
        chip_ecc_SBA_4 = 1
    chip_ecc_ours_4 -= 1
    chip_ecc_SBA_4 -= 1
    chip_ecc_ours_8 -= 1
    chip_ecc_SBA_8 -= 1
    ours_res[dataset_str] = list_to_percent([[chip_ber_ours_4, chip_ecc_ours_4], 
                            [chip_ber_ours_8, chip_ecc_ours_8]])
    sba_res[dataset_str] = list_to_percent([[chip_ber_SBA_4, chip_ecc_SBA_4],
                            [chip_ber_SBA_8, chip_ecc_SBA_8]])
    delta_ber[dataset_str] = list_to_percent([compute_abs_rel(chip_ber_ours_4, chip_ber_SBA_4),
                            compute_abs_rel(chip_ber_ours_8, chip_ber_SBA_8)])
    delta_ecc[dataset_str] = list_to_percent([compute_abs_rel(chip_ecc_ours_4, chip_ecc_SBA_4),
                            compute_abs_rel(chip_ecc_ours_8, chip_ecc_SBA_8)])

def fill_dict():
    filldata("originalchip", originalchip)
    filldata("emberchip", emberchip)
    filldata("emberchiptwo", emberchiptwo)

def compute_comparison(now, original):
    val = original - now
    if val > 0:
        return "+" + "%.2g" % (val * 100) + "%"
    elif val < 0:
        val = -val
        return "-" + "%.2g" % (val * 100) + "%"
    else:
        return "0%"

def to_percent(x):
    if x == 1:
        return "100%"
    if x == -1:
        return "-100%"
    if x == 'N/A':
        return "N/A"
    if x == 0:
        return "0%"
    return ("%.2g" % (x * 100)) + "%"


def compute_fstr(x,bpc_idx):
    bpc = 2 if bpc_idx == 0 else 3
    # bpc_idx = 0 : 2bpc
    # bpc_idx = 1 : 3bpc
    #' \
    str1 = f'\{x},{bpc},{sba_res[x][bpc_idx][0]},{ours_res[x][bpc_idx][0]},{delta_ber[x][bpc_idx][0]},{delta_ber[x][bpc_idx][1]},' \
                + f'{sba_res[x][bpc_idx][1]},{ours_res[x][bpc_idx][1]},{delta_ecc[x][bpc_idx][0]},{delta_ecc[x][bpc_idx][1]}'
    return str1

def report():
    # Hardware	BPC	sba	dala	delta BER	Rel. delta BER	sba	dala	delta ECC	Rel. delta ECC
    print(compute_fstr("originalchip", 0))
    print(compute_fstr("originalchip", 1))
    print(compute_fstr("emberchip", 0))
    print(compute_fstr("emberchip", 1))
    print(compute_fstr("emberchiptwo", 0))
    print(compute_fstr("emberchiptwo", 1))
    

if __name__ == "__main__":
    fill_dict()
    pprint.pprint(ours_res)
    pprint.pprint(sba_res)
    pprint.pprint(delta_ber)
    pprint.pprint(delta_ecc)
    report()