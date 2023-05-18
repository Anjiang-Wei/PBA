   
import matplotlib.pyplot as plt
import numpy as np

# copy from the result of log_trans

# ori_capacity/log_trans

ori_our_res = \
{4: 0.005376344086021501,
 5: 0.027732279760340383,
 6: 0.03679837591602295,
 7: 0.050520354710731415,
 8: 0.07136630250665339}

ori_sba_res = \
{4: 0.01853476639613949,
 5: 0.04037113402061856,
 6: 0.03758010209623112,
 7: 0.08822923108637395,
 8: 0.11275252525252524}

ember_our_res = \
{4: 0.0,
 5: 0.0014705882352941124,
 6: 0.0018382352941176405,
 7: 0.006740196078431349,
 8: 0.011386846405228732}

ember_sba_res = \
{4: 0.0009191176470588203,
 5: 0.004411764705882337,
 6: 0.006740196078431349,
 7: 0.012021475256769363,
 8: 0.02226307189542484}

ember2_our_res = \
{4: 0.0,
 5: 0.0014705882352941124,
 6: 0.00735294117647058,
 7: 0.0015756302521008347,
 8: 0.011029411764705871}

ember2_sba_res = \
{4: 0.0,
 5: 0.003676470588235281,
 6: 0.005514705882352922,
 7: 0.016281512605042008,
 8: 0.021139705882352935}


# set width of bar

fig = plt.subplots(figsize =(15, 10))
 
# set height of bar
ori = [ori_our_res[i] / ori_sba_res[i] for i in range(4, 9)]
ember = [ember_our_res[i] / ember_sba_res[i] for i in range(4, 9)]
ember2 = [ember2_our_res[i] / ember2_sba_res[i] if ember2_sba_res[i] != 0 else 1.0 for i in range(4, 9)]


x = [i for i in range(0, 5)]
labels = [str(i) for i in range(4, 9)]
plt.xticks(x, labels, fontsize=25)

# Adding Xticks
plt.xlabel('Number of Levels', fontsize=25)

plt.yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4], fontsize=25)
plt.ylabel('Relative Level Drift Error w.r.t. SBA', fontsize=25)
# plt.ylim([0, 1.1])


plt.axhline(1.0, linestyle="--", linewidth=4, color='black')
plt.text(-0.1, 1.03, "SBA", size=25) #, bbox=dict(alpha=0.2))


plt.plot(x, ori, "--x", label="TSMC", linewidth=5, markersize=16)
plt.plot(x, ember, "--o", label="EMBER", linewidth=5, markersize=16)
plt.plot(x, ember2, "--^", label="EMBER2", linewidth=5, markersize=16)

plt.legend(fontsize=30)

# plt.show()
plt.savefig('drift_compare.png', bbox_inches='tight')
