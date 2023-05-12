our_res = \
{4: 0.0,
 5: 0.0014705882352941124,
 6: 0.0018382352941176405,
 7: 0.006740196078431349,
 8: 0.011386846405228732}
sba_res = \
{4: 0.0009191176470588203,
 5: 0.004411764705882337,
 6: 0.006740196078431349,
 7: 0.012021475256769363,
 8: 0.02226307189542484}
sba_our_search = \
{4: 0.0009191176470588203,
 5: 0.00588235294117645,
 6: 0.030024509803921556,
 7: 0.08771008403361343,
 8: 0.0785845588235294}
sba_our_search_mean = \
{4: 0.0009191176470588203,
 5: 0.003676470588235281,
 6: 0.007965686274509776,
 7: 0.008403361344537816,
 8: 0.022058823529411742}

raw_ber = {\
'ours4' : 0.0,
'ours8' : 0.003795615468409586,
'SBA4' : 0.00045955882352941176,
'SBA8' : 0.007421023965141612,
}

ecc = \
{'Overhead_Ratio_4': 20.87356321839167,
 'Overhead_Ratio_8': 1.3547758284600386,
 'Reduction_in_Overhead_Ratio_4': 0.9520925110132178,
 'Reduction_in_Overhead_Ratio_8': 0.2618705035971221,
 'SBA4': ['RS', 1.0459770114942528, 455, 435, 21, 9, 6.146415343283516e-16],
 'SBA8': ['RS', 1.123456790123457, 455, 405, 51, 9, 3.057793146199105e-15],
 'ours4': ['RS', 1.002202643171806, 455, 454, 2, 9, 0.0],
 'ours8': ['RS', 1.091127098321343, 455, 417, 39, 9, 3.1108264639185265e-15]}

def to_percent(x, full_percenet=False):
    if x == 1 or full_percenet:
        return "100%"
    return ("%.2g" % (x * 100)) + "%"

def compute_overhead(x):
    return "%.2g" % ((x-1) * 100) + "%"

def table1():
    # Technique	Chip	# Levels	Drift Error Rate	Drift Reduction
    for i in range(4, 9):
        print(f"\sba,\emberchip,{i},{to_percent(sba_res[i])},--")
        print(f"\\tool,\emberchip,{i},{to_percent(our_res[i])},{to_percent((sba_res[i] - our_res[i]) / sba_res[i])}")
def extract_overhead(list):
    # input: ['RS', 1.0459770114942528, 455, 435, 21, 9, 6.146415343283516e-16]
    # output: 455 / 435
    return compute_overhead(list[2] / list[3])


def table2():
    # Technique	Chip	Bits-Per-Cell	Bit Error Rate	ECC Overhead	Improvement
    print(f'\sba,\emberchip,2,{to_percent(raw_ber["SBA4"])},{extract_overhead(ecc["SBA4"])},--')
    print(f'\\tool,\emberchip,2,{to_percent(raw_ber["ours4"])},0%,100%')
    print(f'\sba,\emberchip,3,{to_percent(raw_ber["SBA8"])},{extract_overhead(ecc["SBA8"])},--')
    print(f'\\tool,\emberchip,3,{to_percent(raw_ber["ours8"])},{extract_overhead(ecc["ours8"])},{to_percent(ecc["Reduction_in_Overhead_Ratio_8"])}')

if __name__ == "__main__":
    table1()
    print("\n\n")
    table2()

