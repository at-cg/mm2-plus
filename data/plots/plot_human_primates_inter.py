import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Data for the first part (human) with the updated categories
categories = ['(1) Computing anchors', '(2) Chaining (DP recursion)', '(3) Chaining (DP traceback)', '(4) Marking primary chains', '(5) Base-to-base alignment', '(6) Miscellaneous']
runtime_human = [1237.404, 1135.931, 1032.298, 801.616, 783.492, 727.938]  # Runtime in hours for human

# Apply the mapping to shorten the values
value_mm2_human = np.array([0.091, 0.322 + 0.198, 0.025 + 0.021, 0.048, 0.289, 0.007]) * runtime_human[0]
value_mm2_avx_human = np.array([0.095, 0.366 + 0.230, 0.030 + 0.025, 0.055, 0.191, 0.008]) * runtime_human[1]
value_mm2_avx_olp_human = np.array([0.150, 0.366 + 0.213, 0.028 + 0.026, 0.001, 0.206, 0.010]) * runtime_human[2]
value_mm2_hap_chain_human = np.array([0.125, 0.273 + 0.250, 0.039 + 0.032, 0.001, 0.268, 0.013]) * runtime_human[3]
value_mm2_hap_chain_btk_human = np.array([0.131, 0.280 + 0.257, 0.026 + 0.023, 0.001, 0.270, 0.013]) * runtime_human[4]
value_mm2_hap_chain_btk_sort_human = np.array([0.112, 0.274 + 0.268, 0.032 + 0.029, 0.001, 0.283, 0.003]) * runtime_human[5]
data_human = np.array([value_mm2_human, value_mm2_avx_human, value_mm2_avx_olp_human, value_mm2_hap_chain_human, value_mm2_hap_chain_btk_human, value_mm2_hap_chain_btk_sort_human])

# Data for the second part (primates) with the updated categories
runtime_primates = [2146.975, 1911.632, 1668.894, 1229.227, 1174.610, 1174.683]  # Runtime in hours for primates
value_mm2_primates = np.array([0.079, 0.249 + 0.106, 0.016 + 0.012, 0.012, 0.518, 0.004]) * runtime_primates[0]
value_mm2_avx_primates = np.array([0.087, 0.278 + 0.124, 0.020 + 0.018, 0.016, 0.453, 0.005]) * runtime_primates[1]
value_mm2_olp_primates = np.array([0.092, 0.313 + 0.133, 0.022 + 0.019, 0.000, 0.414, 0.007]) * runtime_primates[2]
value_mm2_hap_chain_primates = np.array([0.131, 0.095 + 0.080, 0.034 + 0.032, 0.001, 0.617, 0.010]) * runtime_primates[3]
value_mm2_hap_chain_btk_primates = np.array([0.140, 0.104 + 0.084, 0.014 + 0.011, 0.001, 0.635, 0.011]) * runtime_primates[4]
value_mm2_hap_chain_btk_sort_primates = np.array([0.111, 0.096 + 0.080, 0.017 + 0.014, 0.001, 0.677, 0.004]) * runtime_primates[5]
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

# Add runtime labels for human
for i, v in enumerate(runtime_human):
    ax1.text(i - 0.25, bottom_human[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Plot bars for primates data
bottom_primates = np.zeros(len(runtime_primates))
for i, category in enumerate(categories):
    ax2.bar(range(len(runtime_primates)), data_primates[:, i], bottom=bottom_primates, color=colors[i], zorder=3)
    bottom_primates += data_primates[:, i]

# Add runtime labels for primates
for i, v in enumerate(runtime_primates):
    ax2.text(i - 0.25, bottom_primates[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=15)

# Set titles for both subplots
ax1.set_title('(C) Human-Human', fontsize=19)
ax2.set_title('(D) Human-Bonobo', fontsize=19)

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

# add yticks as [runtime[0], runtime[1], runtime[2], ...]/3600
ax1.set_yticks(range(0, int(max(bottom_human) + 100), 500))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_human) + 100), 500)], fontsize=17)
ax2.set_yticks(range(0, int(max(bottom_primates) + 100), 500))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_primates) + 100), 500)], fontsize=17)

ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=18)
ax2.set_xlabel('Optimizations', fontsize=18)

# Adding a shared legend at the top
# fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.10), fontsize=12, ncol=6)
plt.tight_layout()
plt.savefig('combined_human_primates_rt1.pdf', bbox_inches='tight', format='pdf', dpi=1200)
