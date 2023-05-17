import numpy as np
import pprint

def get_matrix_from_file(filename):
    with open(filename, "r") as fin:
        lines = fin.readlines()
        n = len(lines)
        matrix = np.zeros((n, n))
        for i in range(n):
            line = list((map(float, lines[i].split(","))))
            assert len(line) == n
            for j in range(n):
                matrix[i][j] = line[j]
    return matrix

# def write_matrix(matrix, filename):
#     with open(filename, "w") as fout:
#         to_write = []
#         for i in range(len(matrix)):
#             to_write.append(",".join(map(str, matrix[i])) + "\n")
#         fout.writelines(to_write)

def compute_average(matrix):
    error_rate = 0
    for i in range(len(matrix)):
        error_rate += 1 - matrix[i][i]
    error_rate = error_rate / len(matrix)
    return error_rate
            
def report_results(filename_prefix, hint):
    res = {}
    for i in range(4, 9):
        fname = filename_prefix + str(i)
        matrix = get_matrix_from_file(fname)
        avg = compute_average(matrix)
        res[i] = avg
    print(hint + " = \\")
    pprint.pprint(res)
    return res

def report_drift_reduction(queries):
    for item in queries:
        our, sba, hint = item
        assert len(our) == len(sba)
        reduce_list = []
        for i in range(4, 9):
            reduce_list.append((sba[i] - our[i]) / sba[i])
        reduce_avg = sum(reduce_list) / len(reduce_list)
        print(f"{hint} Drift Reduction", reduce_list)
        print(f"{hint} Average Drift Reduction", reduce_avg)

gray_coding = \
{
    4: ["00", "01", "11", "10"],
    8: ["000", "001", "011", "010", "110", "111", "101", "100"]
}
dist_4 = np.zeros((4, 4))
dist_8 = np.zeros((8, 8))

def str_diff(s1, s2):
    assert len(s1) == len(s2)
    diff = 0
    for i in range(0, len(s1)):
        if s1[i] != s2[i]:
            diff += 1
    assert diff <= len(s1)
    return diff

def init_dist():
    for i in range(0, 4):
        for j in range(0, 4):
            dist_4[i][j] = str_diff(gray_coding[4][i], gray_coding[4][j])
    for i in range(0, 8):
        for j in range(0, 8):
            dist_8[i][j] = str_diff(gray_coding[8][i], gray_coding[8][j])
    # pprint.pprint(dist_4)
    # pprint.pprint(dist_8)

def report_ber(filename_prefix, level_list, hint=None):
    res = []
    for i in level_list:
        dist = 0
        num_bits = 0
        if i == 4:
            dist = dist_4
            num_bits = 2
        elif i == 8:
            dist = dist_8
            num_bits = 3
        else:
            assert False
        fname = filename_prefix + str(i)
        matrix = get_matrix_from_file(fname)
        ber_matrix = np.multiply(matrix, dist) / i
        # pprint.pprint(ber_matrix)
        ber_avg = np.sum(ber_matrix) / num_bits
        if hint is None:
            print("'" + filename_prefix + str(i) + "' :", str(ber_avg)+",")
        else:
            print("'" + hint + str(i) + "' :", str(ber_avg)+",")
        res.append(ber_avg)
    return res

def report_ber_reduction(our, sba, hint):
    assert len(our) == len(sba)
    for i in range(0, len(our)):
        print(f"BER reduction for level{hint[i]} =", (sba[i] - our[i]) / sba[i])

if __name__ == "__main__":
    ours_drift = report_results("ours", "our_res")
    sba_drift = report_results("SBA", "sba_res")
    our_sigma = report_results("SBAvar", "sba_our_search")
    our_norm = report_results("SBAmeanvar", "sba_our_search_mean")
    report_drift_reduction([(ours_drift, sba_drift, "Overall"), 
                            (ours_drift, our_sigma, "RDR"), 
                            (ours_drift, our_norm, "Non-Normal")])
# we should use this file for final results reported in the paper
# instead of scheme_analyze.py (which is non-uniform weighted average)
    init_dist()
    print("raw_ber = {\\")
    ours_ber = report_ber("ours", [4, 8])
    sba_ber = report_ber("SBA", [4, 8])
    sba_ber = report_ber("SBAmeanvar", [4, 8], hint="norm")
    print("}")
    report_ber_reduction(ours_ber, sba_ber, ["4", "8"])
