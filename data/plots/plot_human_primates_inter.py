import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams.update({'font.size': 12})  # Base font size scaled by 1.2

# Data for the first part (human)
categories = ['Minimizer lookup', 'Chaining 1', 'Backtracking 1', 'Chaining 2', 'Backtracking 2', 'Overlap finding', 'Extension', 'Miscellaneous']
runtime_human = [1237.404, 1135.931, 1032.298, 801.616, 783.492, 727.938]
value_mm2_human = np.array([0.091, 0.322, 0.025, 0.198, 0.021, 0.048, 0.289, 0.007]) * runtime_human[0] / runtime_human[0]
value_mm2_avx_human = np.array([0.095, 0.366, 0.030, 0.230, 0.025, 0.055, 0.191, 0.008]) * runtime_human[1] / runtime_human[0]
value_mm2_avx_olp_human = np.array([0.150, 0.366, 0.028, 0.213, 0.026, 0.001, 0.206, 0.010]) * runtime_human[2] / runtime_human[0]
value_mm2_hap_chain_human = np.array([0.125, 0.273, 0.039, 0.250, 0.032, 0.001, 0.268, 0.013]) * runtime_human[3] / runtime_human[0]
value_mm2_hap_chain_btk_human = np.array([0.131, 0.280, 0.026, 0.257, 0.023, 0.001, 0.270, 0.013]) * runtime_human[4] / runtime_human[0]
value_mm2_hap_chain_btk_sort_human = np.array([0.112, 0.274, 0.032, 0.268, 0.029, 0.001, 0.283, 0.003]) * runtime_human[5] / runtime_human[0]
data_human = np.array([value_mm2_human, value_mm2_avx_human, value_mm2_avx_olp_human, value_mm2_hap_chain_human, value_mm2_hap_chain_btk_human, value_mm2_hap_chain_btk_sort_human])

# Data for the second part (primates)
runtime_primates = [2040.404, 1752.056, 1715.094, 1167.523, 1152.008, 1116.460]
value_mm2_primates = np.array([0.078, 0.256, 0.020, 0.123, 0.017, 0.012, 0.490, 0.005]) * runtime_primates[0] / runtime_primates[0]
value_mm2_avx_primates = np.array([0.084, 0.295, 0.022, 0.146, 0.019, 0.017, 0.412, 0.005]) * runtime_primates[1] / runtime_primates[0]
value_mm2_olp_primates = np.array([0.118, 0.305, 0.023, 0.148, 0.022, 0.000, 0.377, 0.007]) * runtime_primates[2] / runtime_primates[0]
value_mm2_hap_chain_primates = np.array([0.123, 0.114, 0.042, 0.092, 0.039, 0.001, 0.579, 0.010]) * runtime_primates[3] / runtime_primates[0]
value_mm2_hap_chain_btk_primates = np.array([0.127, 0.124, 0.016, 0.097, 0.012, 0.001, 0.613, 0.011]) * runtime_primates[4] / runtime_primates[0]
value_mm2_hap_chain_btk_sort_primates = np.array([0.106, 0.114, 0.019, 0.097, 0.015, 0.001, 0.646, 0.003]) * runtime_primates[5] / runtime_primates[0]
data_primates = np.array([value_mm2_primates, value_mm2_avx_primates, value_mm2_olp_primates, value_mm2_hap_chain_primates, value_mm2_hap_chain_btk_primates, value_mm2_hap_chain_btk_sort_primates])

# Combine human and primates data
data_combined = np.concatenate((data_human, data_primates), axis=1)

# Labels for the bars
labels_human = ['MM2', 'MM2_AVX', 'MM2_OLP', 'MM2_HAP_CHAIN', 'MM2_HAP_CHAIN_BTK', 'MM2_HAP_CHAIN_BTK_SORT']
labels_primates = ['MM2', 'MM2_AVX', 'MM2_OLP', 'MM2_HAP_CHAIN', 'MM2_HAP_CHAIN_BTK', 'MM2_HAP_CHAIN_BTK_SORT']

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 3.5))

# Combine all labels for human and primates
labels_combined = labels_human + labels_primates

# Use a colormap for consistent colors
colors = sns.color_palette("tab10", len(categories))

# Plot bars for human and primates using the same color scheme
bottom_human = np.zeros(len(labels_human))
bottom_primates = np.zeros(len(labels_primates))
for i, category in enumerate(categories):
    # Plot human data
    ax.bar(range(len(labels_human)), data_human[:, i], bottom=bottom_human, label=category, color=colors[i], zorder=3)
    bottom_human += data_human[:, i]
    
    # Plot primates data with offset on the x-axis
    ax.bar(np.arange(len(labels_primates)) + len(labels_human) + 1, data_primates[:, i], bottom=bottom_primates, color=colors[i], zorder=3)
    bottom_primates += data_primates[:, i]

# find the maximum value for the y-axis for each bar in the combined data


# Fix the speedup for human
speedup_human = [runtime_human[0] / x for x in runtime_human]
for i, v in enumerate(speedup_human):
    ax.text(i - 0.25, runtime_human[i] / runtime_human[0] + 0.02, f'{v:.2f}' + 'x', color='black', fontweight='bold', fontsize=9)

# Fix the speedup for primates
speedup_primates = [runtime_primates[0] / x for x in runtime_primates]
for i, v in enumerate(speedup_primates):
    ax.text(i + len(labels_human) + 1 - 0.25, runtime_primates[i] / runtime_primates[0] + 0.02, f'{v:.2f}' + 'x', color='black', fontweight='bold', fontsize=9)

# Add a thick vertical dashed line between human and primates data
ax.axvline(x=len(labels_human), color='black', linestyle='--', linewidth=2)

# Adding legend
ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1))

# Set x-tick labels
ax.set_xticks(np.arange(len(labels_human) + len(labels_primates) + 1))
ax.set_xticklabels(labels_human + [''] + labels_primates, rotation=45, ha='right')
xlabels = ['base', 'A', 'AO', 'AOC', 'AOCB', 'AOCBS', '' , 'base', 'A', 'AO', 'AOC', 'AOCB', 'AOCBS']

ax.text(3, 1.03, 'D_Human', fontsize=11, fontweight='bold', ha='center')
ax.text(10, 1.03, 'D_Primates', fontsize=11, fontweight='bold', ha='center')

# Adding labels and title
ax.set_ylabel('Normalized runtime', fontsize=14)
ax.set_xlabel('Optimizations', fontsize=14)
ax.set_xticklabels(xlabels, rotation=0, ha='center')
plt.ylim(0, 1.1)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', zorder=0)

# Save the figure
plt.savefig('combined_human_primates_rt1.pdf', bbox_inches='tight', format='pdf', dpi=1200)

plt.show()
