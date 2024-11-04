import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Updated categories based on the mapping
categories = ['(1) Computing anchors', '(2) Chaining ', '(3) Marking primary chains', '(4) Base-to-base alignment', '(5) Miscellaneous']

# Data for maize with updated categories
runtime_maize = [15111.068, 14755.744, 10495.920, 3675.419, 3380.453]  # in seconds
value_mm2_maize = np.array([0.024, 0.246 + 0.222 + 0.052 + 0.052, 0.333, 0.053, 0.017]) * runtime_maize[0]
value_mm2_avx_maize = np.array([0.025, 0.252 + 0.224 + 0.055 + 0.055, 0.339, 0.032, 0.017]) * runtime_maize[1]
value_mm2_olp_maize = np.array([0.046, 0.386 + 0.335 + 0.085 + 0.081, 0.0024, 0.046, 0.018]) * runtime_maize[2]
value_mm2_hap_chain_btk_maize = np.array([0.233, 0.179 + 0.169 + 0.042 + 0.040, 0.012, 0.228, 0.096]) * runtime_maize[3]
value_mm2_hap_chain_btk_sort_maize = np.array([0.117, 0.219 + 0.206 + 0.067 + 0.059, 0.014, 0.284, 0.033]) * runtime_maize[4]
data_maize = np.array([value_mm2_maize, value_mm2_avx_maize, value_mm2_olp_maize, value_mm2_hap_chain_btk_maize, value_mm2_hap_chain_btk_sort_maize])

# Data for barley with updated categories
runtime_barley = [42612.805, 41985.786, 26910.393, 7651.801, 6063.077]  # in seconds
value_mm2_barley = np.array([0.036, 0.287 + 0.169 + 0.039 + 0.035, 0.327, 0.094, 0.012]) * runtime_barley[0]
value_mm2_avx_barley = np.array([0.029, 0.289 + 0.170 + 0.038 + 0.035, 0.333, 0.095, 0.012]) * runtime_barley[1]
value_mm2_olp_barley = np.array([0.061, 0.444 + 0.262 + 0.064 + 0.058, 0.003, 0.092, 0.016]) * runtime_barley[2]
value_mm2_hap_chain_btk_barley = np.array([0.221, 0.161 + 0.120 + 0.041 + 0.041, 0.010, 0.348, 0.057]) * runtime_barley[3]
value_mm2_hap_chain_btk_sort_barley = np.array([0.077, 0.203 + 0.142 + 0.054 + 0.053, 0.013, 0.445, 0.014]) * runtime_barley[4]
data_barley = np.array([value_mm2_barley, value_mm2_avx_barley, value_mm2_olp_barley, value_mm2_hap_chain_btk_barley, value_mm2_hap_chain_btk_sort_barley])

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4), sharey=False)

# Use a colormap for consistent colors
colors = sns.color_palette("tab10", len(categories))

# Plot bars for barley data (swap this to ax1)
bottom_barley = np.zeros(len(runtime_barley))
for i, category in enumerate(categories):
    ax1.bar(range(len(runtime_barley)), data_barley[:, i], bottom=bottom_barley, label=category, color=colors[i], zorder=3)
    bottom_barley += data_barley[:, i]

# Add runtime labels for barley (in hours)
for i, v in enumerate(runtime_barley):
    ax1.text(i - 0.25, bottom_barley[i] + 1000, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Plot bars for maize data (swap this to ax2)
bottom_maize = np.zeros(len(runtime_maize))
for i, category in enumerate(categories):
    ax2.bar(range(len(runtime_maize)), data_maize[:, i], bottom=bottom_maize, color=colors[i], zorder=3)
    bottom_maize += data_maize[:, i]

# Add runtime labels for maize (in hours)
for i, v in enumerate(runtime_maize):
    ax2.text(i - 0.25, bottom_maize[i] + 500, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Set titles for both subplots (swap titles)
ax1.set_title('(A) Barley-Barley', fontsize=19)  # Swapped to ax1
ax2.set_title('(B) Maize-Maize', fontsize=19)    # Swapped to ax2

# Set y-axis labels
ax1.set_ylabel('Runtime (hours)', fontsize=18)
ax2.set_ylabel('  ', fontsize=18)

# Set x-tick labels for barley and maize (swap labels)
ax1.set_xticks(range(len(runtime_barley)))
ax1.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$'], rotation=0, fontsize=17)

ax2.set_xticks(range(len(runtime_maize)))
ax2.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$'], rotation=0, fontsize=17)

# Adjust y-limits to be non-normalized
ax1.set_ylim(0, max(bottom_barley) + 5000)
ax2.set_ylim(0, max(bottom_maize) + 3000)

# Add yticks as runtime in hours
ax1.set_yticks(range(0, int(max(bottom_barley) + 1000), 10000))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_barley) + 1000), 10000)], fontsize=17)
ax2.set_yticks(range(0, int(max(bottom_maize) + 1000), 5000))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_maize) + 1000), 5000)], fontsize=17)

# Grid lines for y-axis
ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# Set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=18)
ax2.set_xlabel('Optimizations', fontsize=18)

# Adding a shared legend at the top
fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.22), fontsize=17, ncol=3)

plt.tight_layout()
plt.savefig('combined_maize_barley.pdf', bbox_inches='tight', format='pdf', dpi=1200)
