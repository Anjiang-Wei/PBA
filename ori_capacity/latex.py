our_res = \
{4: 0.005376344086021501,
 5: 0.027732279760340383,
 6: 0.03679837591602295,
 7: 0.050520354710731415,
 8: 0.07136630250665339}
sba_res = \
{4: 0.01853476639613949,
 5: 0.04037113402061856,
 6: 0.03758010209623112,
 7: 0.08822923108637395,
 8: 0.11275252525252524}
sba_our_search = \
{4: 0.03063854407742478,
 5: 0.034060606060606055,
 6: 0.051132146600509486,
 7: 0.0716536667264551,
 8: 0.08731699201419699}
sba_our_search_mean = \
{4: 0.010101010101010083,
 5: 0.028634546602146017,
 6: 0.048749999999999995,
 7: 0.061630213093291704,
 8: 0.10434661891471461}

raw_ber = {\
'ours4' : 0.002688172043010753,
'ours8' : 0.023788767502217794,
'SBA4' : 0.009267383198069752,
'SBA8' : 0.033796296296296297,
}

ecc = \
{'Overhead_Ratio_4': 1.6917082294264327,
 'Overhead_Ratio_8': 1.2749501661129572,
 'Reduction_in_Overhead_Ratio_4': 0.4088815183342543,
 'Reduction_in_Overhead_Ratio_8': 0.21565561809464273,
 'SBA4': ['RS', 1.1346633416458853, 455, 401, 55, 9, 9.63968522835173e-15],
 'SBA8': ['RS', 1.2971428571428572, 454, 350, 105, 9, 9.840997955964647e-15],
 'ours4': ['RS', 1.0796019900497513, 434, 402, 33, 9, 9.763133351858996e-15],
 'ours8': ['RS', 1.2330623306233062, 455, 369, 87, 9, 9.248820413693536e-15]}

def to_percent(x, full_percenet=False):
    if x == 1 or full_percenet:
        return "100%"
    return ("%.2g" % (x * 100)) + "%"

def compute_overhead(x):
    return "%.2g" % ((x-1) * 100) + "%"

def table1():
    # Technique	Chip	# Levels	Drift Error Rate	Drift Reduction
    for i in range(4, 9):
        print(f"\sba,\originalchip,{i},{to_percent(sba_res[i])},--")
        print(f"\\tool,\originalchip,{i},{to_percent(our_res[i])},{to_percent((sba_res[i] - our_res[i]) / sba_res[i])}")
def extract_overhead(list):
    # input: ['RS', 1.0459770114942528, 455, 435, 21, 9, 6.146415343283516e-16]
    # output: 455 / 435
    return compute_overhead(list[2] / list[3])


def table2():
    # Technique	Chip	Bits-Per-Cell	Bit Error Rate	ECC Overhead	Improvement
    print(f'\sba,\originalchip,2,{to_percent(raw_ber["SBA4"])},{extract_overhead(ecc["SBA4"])},--')
    print(f'\\tool,\originalchip,2,{to_percent(raw_ber["ours4"])},{extract_overhead(ecc["ours4"])},{to_percent(ecc["Reduction_in_Overhead_Ratio_4"])}')
    print(f'\sba,\originalchip,3,{to_percent(raw_ber["SBA8"])},{extract_overhead(ecc["SBA8"])},--')
    print(f'\\tool,\originalchip,3,{to_percent(raw_ber["ours8"])},{extract_overhead(ecc["ours8"])},{to_percent(ecc["Reduction_in_Overhead_Ratio_8"])}')

if __name__ == "__main__":
    table1()
    print("\n\n")
    table2()

