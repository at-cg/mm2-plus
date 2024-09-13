import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams.update({'font.size': 12})  # Base font size scaled by 1.2

# Updated categories based on the mapping
categories = ['Computing anchors', 'Chaining (DP recursion)', 'Chaining (DP traceback)', 'Filtering primary chains', 'Base-to-base alignment', 'Miscellaneous']

# Data for maize with updated categories
runtime_maize = [15182.391, 14358.611, 11304.108, 4452.148, 2648.973, 2280.432]  # in seconds
value_mm2_maize = np.array([0.025, 0.263 + 0.236, 0.057 + 0.057, 0.289, 0.055, 0.017]) * runtime_maize[0]
value_mm2_avx_maize = np.array([0.026, 0.280 + 0.250, 0.056 + 0.053, 0.284, 0.035, 0.016]) * runtime_maize[1]
value_mm2_olp_maize = np.array([0.046, 0.378 + 0.337, 0.088 + 0.083, 0.002, 0.047, 0.019]) * runtime_maize[2]
value_mm2_hap_chain_maize = np.array([0.118, 0.091 + 0.086, 0.266 + 0.256, 0.006, 0.127, 0.050]) * runtime_maize[3]
value_mm2_hap_chain_btk_maize = np.array([0.205, 0.170 + 0.159, 0.078 + 0.069, 0.011, 0.221, 0.088]) * runtime_maize[4]
value_mm2_hap_chain_btk_sort_maize = np.array([0.096, 0.193 + 0.196, 0.126 + 0.090, 0.014, 0.261, 0.023]) * runtime_maize[5]
data_maize = np.array([value_mm2_maize, value_mm2_avx_maize, value_mm2_olp_maize, value_mm2_hap_chain_maize, value_mm2_hap_chain_btk_maize, value_mm2_hap_chain_btk_sort_maize])

# Data for barley with updated categories
runtime_barley = [46035.151, 45560.924, 26910.393, 10761.150, 7651.801, 6063.077]  # in seconds
value_mm2_barley = np.array([0.027, 0.272 + 0.161, 0.044 + 0.041, 0.354, 0.089, 0.012]) * runtime_barley[0]
value_mm2_avx_barley = np.array([0.027, 0.274 + 0.159, 0.042 + 0.040, 0.383, 0.061, 0.013]) * runtime_barley[1]
value_mm2_olp_barley = np.array([0.061, 0.444 + 0.262, 0.064 + 0.058, 0.003, 0.092, 0.016]) * runtime_barley[2]
value_mm2_hap_chain_barley = np.array([0.154, 0.112 + 0.077, 0.188 + 0.183, 0.007, 0.238, 0.041]) * runtime_barley[3]
value_mm2_hap_chain_btk_barley = np.array([0.221, 0.161 + 0.120, 0.041 + 0.041, 0.010, 0.348, 0.057]) * runtime_barley[4]
value_mm2_hap_chain_btk_sort_barley = np.array([0.077, 0.203 + 0.142, 0.054 + 0.053, 0.013, 0.445, 0.014]) * runtime_barley[5]
data_barley = np.array([value_mm2_barley, value_mm2_avx_barley, value_mm2_olp_barley, value_mm2_hap_chain_barley, value_mm2_hap_chain_btk_barley, value_mm2_hap_chain_btk_sort_barley])

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4), sharey=False)

# Use a colormap for consistent colors
colors = sns.color_palette("tab10", len(categories))

# Plot bars for maize data
bottom_maize = np.zeros(len(runtime_maize))
for i, category in enumerate(categories):
    ax1.bar(range(len(runtime_maize)), data_maize[:, i], bottom=bottom_maize, label=category, color=colors[i], zorder=3)
    bottom_maize += data_maize[:, i]

# Add runtime labels for maize (in hours)
for i, v in enumerate(runtime_maize):
    ax1.text(i - 0.25, bottom_maize[i] + 500, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=11)

# Plot bars for barley data
bottom_barley = np.zeros(len(runtime_barley))
for i, category in enumerate(categories):
    ax2.bar(range(len(runtime_barley)), data_barley[:, i], bottom=bottom_barley, color=colors[i], zorder=3)
    bottom_barley += data_barley[:, i]

# Add runtime labels for barley (in hours)
for i, v in enumerate(runtime_barley):
    ax2.text(i - 0.25, bottom_barley[i] + 1000, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=11)

# Set titles for both subplots
ax1.set_title('(A) Maize-Maize', fontsize=15, fontweight='bold')
ax2.set_title('(B) Barley-Barley', fontsize=15, fontweight='bold')

# Set y-axis labels
ax1.set_ylabel('Runtime in hours', fontsize=15)
ax2.set_ylabel('  ', fontsize=15)

# Set x-tick labels for maize and barley
ax1.set_xticks(range(len(runtime_maize)))
ax1.set_xticklabels(['base', 'A', 'AO', 'AOC', 'AOBC', 'AOBCS'], rotation=0)

ax2.set_xticks(range(len(runtime_barley)))
ax2.set_xticklabels(['base', 'A', 'AO', 'AOC', 'AOBC', 'AOBCS'], rotation=0)

# Adjust y-limits to be non-normalized
ax1.set_ylim(0, max(bottom_maize) + 3000)
ax2.set_ylim(0, max(bottom_barley) + 5000)

# Add yticks as runtime in hours
ax1.set_yticks(range(0, int(max(bottom_maize) + 1000), 5000))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_maize) + 1000), 5000)])
ax2.set_yticks(range(0, int(max(bottom_barley) + 1000), 10000))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_barley) + 1000), 10000)])

# Grid lines for y-axis
ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# Set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=15)
ax2.set_xlabel('Optimizations', fontsize=15)

# Adding a shared legend at the top
fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.10), fontsize=12, ncol=6)

plt.tight_layout()
plt.savefig('combined_maize_barley_rt1.pdf', bbox_inches='tight', format='pdf', dpi=1200)