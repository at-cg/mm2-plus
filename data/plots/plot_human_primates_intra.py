import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Updated categories based on the mapping
categories = ['(1) Computing anchors', '(2) Chaining (DP recursion)', '(3) Chaining (DP traceback)', '(4) Marking primary chains', '(5) Base-to-base alignment', '(6) Miscellaneous']

# Data for Human with updated categories
runtime_human = [1237.404, 1135.931, 1032.298, 941.719, 849.041, 790.252]  # in seconds
value_mm2_human = np.array([0.091, 0.322 + 0.198, 0.025 + 0.021, 0.048, 0.289, 0.007]) * runtime_human[0]
value_mm2_avx_human = np.array([0.095, 0.366 + 0.230, 0.030 + 0.025, 0.055, 0.191, 0.008]) * runtime_human[1]
value_mm2_olp_human = np.array([0.150, 0.366 + 0.213, 0.028 + 0.026, 0.001, 0.206, 0.010]) * runtime_human[2]
value_mm2_hap_chain_human = np.array([0.165, 0.243 + 0.289, 0.035 + 0.029, 0.001, 0.227, 0.011]) * runtime_human[3]
value_mm2_hap_chain_btk_human = np.array([0.118, 0.266 + 0.316, 0.024 + 0.020, 0.001, 0.243, 0.012]) * runtime_human[4]
value_mm2_hap_chain_btk_sort_human = np.array([0.101, 0.247 + 0.320, 0.032 + 0.026, 0.001, 0.271, 0.003]) * runtime_human[5]
data_human = np.array([value_mm2_human, value_mm2_avx_human, value_mm2_olp_human, value_mm2_hap_chain_human, value_mm2_hap_chain_btk_human, value_mm2_hap_chain_btk_sort_human])

# Data for Primates with updated categories
runtime_primates = [2146.975, 1911.632, 1668.894, 1546.090, 1451.113, 1386.812]  # in seconds
value_mm2_primates = np.array([0.079, 0.249 + 0.106, 0.016 + 0.012, 0.012, 0.518, 0.004]) * runtime_primates[0]
value_mm2_avx_primates = np.array([0.087, 0.278 + 0.124, 0.020 + 0.018, 0.016, 0.453, 0.005]) * runtime_primates[1]
value_mm2_olp_primates = np.array([0.092, 0.313 + 0.133, 0.022 + 0.019, 0.000, 0.414, 0.007]) * runtime_primates[2]
value_mm2_hap_chain_primates = np.array([0.118, 0.164 + 0.138, 0.035 + 0.028, 0.001, 0.509, 0.008]) * runtime_primates[3]
value_mm2_hap_chain_btk_primates = np.array([0.129, 0.178 + 0.146, 0.015 + 0.011, 0.001, 0.513, 0.008]) * runtime_primates[4]
value_mm2_hap_chain_btk_sort_primates = np.array([0.107, 0.174 + 0.144, 0.019 + 0.013, 0.001, 0.540, 0.004]) * runtime_primates[5]
data_primates = np.array([value_mm2_primates, value_mm2_avx_primates, value_mm2_olp_primates, value_mm2_hap_chain_primates, value_mm2_hap_chain_btk_primates, value_mm2_hap_chain_btk_sort_primates])

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 4), sharey=False)

# Use a colormap for consistent colors
colors = sns.color_palette("tab10", len(categories))

# Plot bars for human data
bottom_human = np.zeros(len(runtime_human))
for i, category in enumerate(categories):
    ax1.bar(range(len(runtime_human)), data_human[:, i], bottom=bottom_human, label=category, color=colors[i], zorder=3)
    bottom_human += data_human[:, i]

# Add runtime labels for human (in hours)
for i, v in enumerate(runtime_human):
    ax1.text(i - 0.25, bottom_human[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Plot bars for primates data
bottom_primates = np.zeros(len(runtime_primates))
for i, category in enumerate(categories):
    ax2.bar(range(len(runtime_primates)), data_primates[:, i], bottom=bottom_primates, color=colors[i], zorder=3)
    bottom_primates += data_primates[:, i]

# Add runtime labels for primates (in hours)
for i, v in enumerate(runtime_primates):
    ax2.text(i - 0.25, bottom_primates[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Set titles for both subplots
ax1.set_title('(C) Human-Human', fontsize=18)
ax2.set_title('(D) Human-Bonobo', fontsize=18)

# Set y-axis labels
ax1.set_ylabel('Runtime (hours)', fontsize=18)
ax2.set_ylabel('  ', fontsize=18)

# Set x-tick labels for human and primates
ax1.set_xticks(range(len(runtime_human)))
ax1.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$', '$+O_5$'], rotation=0, fontsize=17)

ax2.set_xticks(range(len(runtime_primates)))
ax2.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$', '$+O_5$'], rotation=0, fontsize=17)

# Adjust y-limits to be non-normalized
ax1.set_ylim(0, max(bottom_human) + 200)
ax2.set_ylim(0, max(bottom_primates) + 200)

# Add yticks as runtime in hours
ax1.set_yticks(range(0, int(max(bottom_human) + 100), 500))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_human) + 100), 500)], fontsize=17)
ax2.set_yticks(range(0, int(max(bottom_primates) + 100), 500))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_primates) + 100), 500)], fontsize=17)

# Grid lines for y-axis
ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# Set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=18)
ax2.set_xlabel('Optimizations', fontsize=18)

# Adding a shared legend at the top
# fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.10), fontsize=12, ncol=6)

plt.tight_layout()
plt.savefig('combined_human_primates_rt2.pdf', bbox_inches='tight', format='pdf', dpi=1200)
