our_res = \
{4: 0.0,
 5: 0.0014705882352941124,
 6: 0.00735294117647058,
 7: 0.0015756302521008347,
 8: 0.011029411764705871}
sba_res = \
{4: 0.0,
 5: 0.003676470588235281,
 6: 0.005514705882352922,
 7: 0.016281512605042008,
 8: 0.021139705882352935}
sba_our_search = \
{4: 0.0,
 5: 0.002941176470588225,
 6: 0.006740196078431367,
 7: 0.01628151260504202,
 8: 0.028952205882352935}
sba_our_search_mean = \
{4: 0.0,
 5: 0.0014705882352941124,
 6: 0.0030637254901960675,
 7: 0.010504201680672263,
 8: 0.02389705882352941}

raw_ber = {\
'ours4' : 0.0,
'ours8' : 0.0036764705882352936,
'SBA4' : 0.0,
'SBA8' : 0.0070465686274509805,
}

ecc = \
{'Overhead_Ratio_4': 1.0,
 'Overhead_Ratio_8': 1.3071253071253082,
 'Reduction_in_Overhead_Ratio_4': 0.0,
 'Reduction_in_Overhead_Ratio_8': 0.2349624060150382,
 'SBA4': ['RS', 1.002202643171806, 455, 454, 2, 9, 0.0],
 'SBA8': ['RS', 1.117936117936118, 455, 407, 49, 9, 7.957814271246027e-15],
 'ours4': ['RS', 1.002202643171806, 455, 454, 2, 9, 0.0],
 'ours8': ['RS', 1.0902255639097744, 435, 399, 37, 9, 9.667004789228045e-15]}

def to_percent(x, full_percenet=False):
    if x == 1 or full_percenet:
        return "100%"
    return ("%.2g" % (x * 100)) + "%"

def compute_overhead(x):
    return "%.2g" % ((x-1) * 100) + "%"

def table1():
    # Technique	Chip	# Levels	Drift Error Rate	Drift Reduction
    print(f'\sba,\emberchip2,4,0%,--')
    print(f'\\tool,\emberchip2,4,0%,0%')
    for i in range(5, 9):
        print(f"\sba,\emberchip2,{i},{to_percent(sba_res[i])},--")
        print(f"\\tool,\emberchip2,{i},{to_percent(our_res[i])},{to_percent((sba_res[i] - our_res[i]) / sba_res[i])}")
def extract_overhead(list):
    # input: ['RS', 1.0459770114942528, 455, 435, 21, 9, 6.146415343283516e-16]
    # output: 455 / 435
    return compute_overhead(list[2] / list[3])


def table2():
    # Technique	Chip	Bits-Per-Cell	Bit Error Rate	ECC Overhead	Improvement
    print(f'\sba,\emberchip2,2,0%,0%,--')
    print(f'\\tool,\emberchip2,2,0%,0%,0%')
    print(f'\sba,\emberchip2,3,{to_percent(raw_ber["SBA8"])},{extract_overhead(ecc["SBA8"])},--')
    print(f'\\tool,\emberchip2,3,{to_percent(raw_ber["ours8"])},{extract_overhead(ecc["ours8"])},{to_percent(ecc["Reduction_in_Overhead_Ratio_8"])}')


def table3():
    # Technique	Chip	# Levels	Drift Error Rate	Improv. w.r.t \toolsigma
    for i in range(4, 9):
        print(f"\\toolsigma,\emberchip2,{i},{to_percent(sba_our_search[i])},--")
        print(f"\\toolnormal,\emberchip2,{i},{to_percent(sba_our_search_mean[i])},{to_percent((sba_our_search[i] - sba_our_search_mean[i]) / sba_our_search[i]) if sba_our_search[i] != 0 else '0%'}")
        print(f"\\tooleval,\emberchip2,{i},{to_percent(our_res[i])},{to_percent((sba_our_search[i] - our_res[i]) / sba_our_search[i]) if sba_our_search[i] != 0 else '0%'}")

if __name__ == "__main__":
    table1()
    print("\n\n")
    table2()
    print("\n\n")
    table3()
