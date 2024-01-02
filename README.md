# PBA Repository
This repository includes the Python scripts for the research paper ["PBA: Percentile-Based Level Allocation for Multiple-Bits-Per-Cell RRAM"](https://cs.stanford.edu/~anjiang/papers/ICCAD23PBA.pdf), at ICCAD'23.

## Hardware Measurement Data
We conduct experiments on two ember chips and measure the resistance at the timestamp of 1 second.

The raw data for ember chip [1](https://github.com/Anjiang-Wei/PBA/blob/dala/data/retention1s.csv) and [2](https://github.com/Anjiang-Wei/PBA/blob/dala/data/retention1s2.csv) are provided.

We then build a more compact representation of the data points with scripts [1](https://github.com/Anjiang-Wei/PBA/blob/dala/analysis/build_retention_model.py) and [2](https://github.com/Anjiang-Wei/PBA/blob/dala/analysis/build_retention_model2.py) respectively, generating two files [1](https://github.com/Anjiang-Wei/PBA/blob/dala/model/retention1s.csv) and [2](https://github.com/Anjiang-Wei/PBA/blob/dala/model/retention1s2.csv) in the format of `write_level_low, write_level_high, (list of levels)` where `list_of_levels` is the readout level index after waiting for 1 second.

## Experiments

### SBA versus PBA
With the SBA [implementation](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/SBA.py), we generate the probability transition matrix with this [script](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/SBA_genmatrix.py), and the matrix is saved [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity) (`SBA4`, `SBA8`) for chip1, and [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity2) (`SBA4`, `SBA8`) for chip2.

The PBA [implementation](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/dala.py). We generate the probability transition matrix with this [script](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/dala_genmatrix.py), and the matrix is saved [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity) (`ours4`, `ours8`) for chip1, and [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity2) (`ours4`, `ours8`) for chip2.

We use gray coding and compute the [bit error rate](https://github.com/Anjiang-Wei/PBA/blob/dala/ember_capacity/trans.py) from the transition matrix. After obtaining the bit error rate results, then we run a [search](https://github.com/Anjiang-Wei/PBA/blob/dala/ember_capacity/ecc.py) to find the error correcting code with the lowest overhead. The expected output is saved in the logs for [BER](https://github.com/Anjiang-Wei/PBA/blob/dala/ember_capacity/log_trans) and [ECC](https://github.com/Anjiang-Wei/PBA/blob/dala/ember_capacity/log_ecc)

### Ablation Study
With the PBA-norm [implementation](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/SBA_meanvariant.py), we can generate the probability transition matrix with this [script](https://github.com/Anjiang-Wei/PBA/blob/dala/algorithm/SBA_genmatrix.py), and the matrix is saved [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity) (`SBAmeanvar4`, `SBAmeanvar8`) for chip1, and [here](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_capacity2) (`SBAmeanvar4`, `SBAmeanvar8`) for chip2. The bit error rate and ECC results can be generated with the corresponding scripts in the same directory as the transition matrix.

### Other Experiments
1) Dataset sizes: [script](https://github.com/Anjiang-Wei/PBA/tree/dala/algorithm_repeatavail) to generate [matrix result](https://github.com/Anjiang-Wei/PBA/tree/dala/ember_repeatavail) with different ratios of the original dataset.
2) Different ratios of target chip and non-target chip:
- a) completely switch the two: [script](https://github.com/Anjiang-Wei/PBA/tree/dala/algorithm_inter) to generate [matrix result](https://github.com/Anjiang-Wei/PBA/tree/dala/intercapacity)
- b) half and half: [script](https://github.com/Anjiang-Wei/PBA/tree/dala/algorithm_both) to generate [matrix result](https://github.com/Anjiang-Wei/PBA/tree/dala/bothcapacity)
- c) one dominates the other: [script](https://github.com/Anjiang-Wei/PBA/tree/dala/algorithm_dominate) to generate [matrix result](https://github.com/Anjiang-Wei/PBA/tree/dala/domin_capacity)

**Note: Directories ending with `2`, e.g., `ember_capacity2`, are for Ember Chip 2. For directories without 2, e.g., `ember_capacity`, are for Ember Chip 1.**
