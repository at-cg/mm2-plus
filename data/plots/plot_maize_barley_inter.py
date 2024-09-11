import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams.update({'font.size': 12})  # Base font size scaled by 1.2

# Data categories
categories = ['Minimizer lookup', 'Chaining 1', 'Backtracking 1', 'Chaining 2', 'Backtracking 2', 'Overlap finding', 'Extension', 'Miscellaneous']

# Data for maize
runtime_maize = [15182.391, 14358.611, 11304.108, 4452.148, 2648.973, 2280.432]
value_mm2_maize = np.array([0.025, 0.263, 0.057, 0.236, 0.057, 0.289, 0.055, 0.017]) * runtime_maize[0] / runtime_maize[0]
value_mm2_avx_maize = np.array([0.026, 0.280, 0.056, 0.250, 0.053, 0.284, 0.035, 0.016]) * runtime_maize[1] / runtime_maize[0]
value_mm2_olp_maize = np.array([0.046, 0.378, 0.088, 0.337, 0.083, 0.002, 0.047, 0.019]) * runtime_maize[2] / runtime_maize[0]
value_mm2_hap_chain_maize = np.array([0.118, 0.091, 0.266, 0.086, 0.256, 0.006, 0.127, 0.050]) * runtime_maize[3] / runtime_maize[0]
value_mm2_hap_chain_btk_maize = np.array([0.205, 0.170, 0.078, 0.159, 0.069, 0.011, 0.221, 0.088]) * runtime_maize[4] / runtime_maize[0]
value_mm2_hap_chain_btk_sort_maize = np.array([0.096, 0.193, 0.126, 0.196, 0.090, 0.014, 0.261, 0.023]) * runtime_maize[5] / runtime_maize[0]
data_maize = np.array([value_mm2_maize, value_mm2_avx_maize, value_mm2_olp_maize, value_mm2_hap_chain_maize, value_mm2_hap_chain_btk_maize, value_mm2_hap_chain_btk_sort_maize])

# Data for barley
runtime_barley = [46035.151, 45560.924, 26910.393, 10761.150, 7651.801, 6063.077]
value_mm2_barley = np.array([0.027, 0.272, 0.044, 0.161, 0.041, 0.354, 0.089, 0.012]) * runtime_barley[0] / runtime_barley[0]
value_mm2_avx_barley = np.array([0.027, 0.274, 0.042, 0.159, 0.040, 0.383, 0.061, 0.013]) * runtime_barley[1] / runtime_barley[0]
value_mm2_olp_barley = np.array([0.061, 0.444, 0.064, 0.262, 0.058, 0.003, 0.092, 0.016]) * runtime_barley[2] / runtime_barley[0]
value_mm2_hap_chain_barley = np.array([0.154, 0.112, 0.188, 0.077, 0.183, 0.007, 0.238, 0.041]) * runtime_barley[3] / runtime_barley[0]
value_mm2_hap_chain_btk_barley = np.array([0.221, 0.161, 0.041, 0.120, 0.041, 0.010, 0.348, 0.057]) * runtime_barley[4] / runtime_barley[0]
value_mm2_hap_chain_btk_sort_barley = np.array([0.077, 0.203, 0.054, 0.142, 0.053, 0.013, 0.445, 0.014]) * runtime_barley[5] / runtime_barley[0]
data_barley = np.array([value_mm2_barley, value_mm2_avx_barley, value_mm2_olp_barley, value_mm2_hap_chain_barley, value_mm2_hap_chain_btk_barley, value_mm2_hap_chain_btk_sort_barley])

# Combine maize and barley data
data_combined = np.concatenate((data_maize, data_barley), axis=1)

# Labels for the bars
labels_maize = ['MM2', 'MM2_AVX', 'MM2_OLP', 'MM2_HAP_CHAIN', 'MM2_HAP_CHAIN_BTK', 'MM2_HAP_CHAIN_BTK_SORT']
labels_barley = ['MM2', 'MM2_AVX', 'MM2_OLP', 'MM2_HAP_CHAIN', 'MM2_HAP_CHAIN_BTK', 'MM2_HAP_CHAIN_BTK_SORT']

# Create figure and axis
fig, ax = plt.subplots(figsize=(12, 3.5))

# Combine all labels for maize and barley
labels_combined = labels_maize + labels_barley

# Use a colormap for consistent colors
colors = sns.color_palette("tab10", len(categories))

# Plot bars for maize and barley using the same color scheme
bottom_maize = np.zeros(len(labels_maize))
bottom_barley = np.zeros(len(labels_barley))
for i, category in enumerate(categories):
    # Plot maize data
    ax.bar(range(len(labels_maize)), data_maize[:, i], bottom=bottom_maize, label=category, color=colors[i], zorder=3)
    bottom_maize += data_maize[:, i]
    
    # Plot barley data with offset on the x-axis
    ax.bar(np.arange(len(labels_barley)) + len(labels_maize) + 1, data_barley[:, i], bottom=bottom_barley, color=colors[i], zorder=3)
    bottom_barley += data_barley[:, i]

# Add speedup for maize
speedup_maize = [runtime_maize[0] / x for x in runtime_maize]
for i, v in enumerate(speedup_maize):
    ax.text(i - 0.25, runtime_maize[i] / runtime_maize[0] + 0.02, f'{v:.2f}' + 'x', color='black', fontweight='bold', fontsize=9)

# Add speedup for barley
speedup_barley = [runtime_barley[0] / x for x in runtime_barley]
for i, v in enumerate(speedup_barley):
    ax.text(i + len(labels_maize) + 1 - 0.25, runtime_barley[i] / runtime_barley[0] + 0.02, f'{v:.2f}' + 'x', color='black', fontweight='bold', fontsize=9)

# Add a thick vertical dashed line between maize and barley data
ax.axvline(x=len(labels_maize), color='black', linestyle='--', linewidth=2)

# Adding legend
ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1))

# Set x-tick labels
ax.set_xticks(np.arange(len(labels_maize) + len(labels_barley) + 1))
ax.set_xticklabels(labels_maize + [''] + labels_barley, rotation=45, ha='right')
xlabels = ['base', 'A', 'AO', 'AOC', 'AOCB', 'AOCBS', '', 'base', 'A', 'AO', 'AOC', 'AOCB', 'AOCBS']

ax.text(3, 1.03, 'D_Maize', fontsize=11, fontweight='bold', ha='center')
ax.text(10, 1.03, 'D_Barley', fontsize=11, fontweight='bold', ha='center')

# Adding labels and title
ax.set_ylabel('Normalized runtime', fontsize=14)
ax.set_xlabel('Optimizations', fontsize=14)
ax.set_xticklabels(xlabels, rotation=0, ha='center')
plt.ylim(0, 1.1)
plt.tight_layout()
plt.grid(axis='y', linestyle='--', zorder=0)

# Save the figure
plt.savefig('combined_maize_barley_rt1.pdf', bbox_inches='tight', format='pdf', dpi=1200)

plt.show()
