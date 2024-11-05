import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Data for the first part (human) with the updated categories
categories = ['(1) Computing anchors', '(2) Chaining', '(3) Marking primary chains', '(4) Base-to-base alignment', '(5) Miscellaneous']
runtime_human = [1175.378, 1033.084, 972.320, 779.279, 723.490]  # Runtime in hours for human

# Apply the mapping to shorten the values
value_mm2_human = np.array([0.098, 0.318 + 0.186 + 0.031 + 0.024, 0.022, 0.313, 0.009]) * runtime_human[0]
value_mm2_avx_human = np.array([0.110, 0.366 + 0.222 + 0.032 + 0.025, 0.026, 0.209, 0.009]) * runtime_human[1]
value_mm2_avx_olp_human = np.array([0.116, 0.382 + 0.222 + 0.032 + 0.027, 0.001, 0.209, 0.011]) * runtime_human[2]
value_mm2_hap_chain_btk_human = np.array([0.140, 0.282 + 0.256 + 0.026 + 0.023, 0.001, 0.259, 0.013]) * runtime_human[3]
value_mm2_hap_chain_btk_sort_human = np.array([0.119, 0.268 + 0.268 + 0.034 + 0.030, 0.001, 0.275, 0.004]) * runtime_human[4]
data_human = np.array([value_mm2_human, value_mm2_avx_human, value_mm2_avx_olp_human, value_mm2_hap_chain_btk_human, value_mm2_hap_chain_btk_sort_human])

# Data for the second part (primates) with the updated categories
runtime_primates = [2171.764, 1751.729, 1674.217, 1224.240, 1158.671]  # Runtime in hours for primates
value_mm2_primates = np.array([0.077, 0.246 + 0.106 + 0.016 + 0.014, 0.012, 0.525, 0.004]) * runtime_primates[0]
value_mm2_avx_primates = np.array([0.093, 0.300 + 0.129 + 0.019 + 0.017, 0.014, 0.424, 0.005]) * runtime_primates[1]
value_mm2_olp_primates = np.array([0.094, 0.309 + 0.134 + 0.022 + 0.019, 0.000, 0.415, 0.007]) * runtime_primates[2]
value_mm2_hap_chain_btk_primates = np.array([0.138, 0.100 + 0.082 + 0.014 + 0.011, 0.001, 0.645, 0.011]) * runtime_primates[3]
value_mm2_hap_chain_btk_sort_primates = np.array([0.110, 0.098 + 0.081 + 0.017 + 0.014, 0.001, 0.676, 0.004]) * runtime_primates[4]
data_primates = np.array([value_mm2_primates, value_mm2_avx_primates, value_mm2_olp_primates, value_mm2_hap_chain_btk_primates, value_mm2_hap_chain_btk_sort_primates])

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
ax1.set_title('(C) Human-Human', fontsize=20)
ax2.set_title('(D) Human-Bonobo', fontsize=20)

# Set y-axis labels
ax1.set_ylabel('Runtime (hours)', fontsize=19)
ax2.set_ylabel('  ', fontsize=19)

# Set x-tick labels for human and primates
ax1.set_xticks(range(len(runtime_human)))
ax1.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$'], rotation=0, fontsize=18)

ax2.set_xticks(range(len(runtime_primates)))
ax2.set_xticklabels(['base', '$+O_1$', '$+O_2$', '$+O_3$', '$+O_4$'], rotation=0, fontsize=18)

# Adjust y-limits to be non-normalized
ax1.set_ylim(0, max(bottom_human) + 200)
ax2.set_ylim(0, max(bottom_primates) + 300)

# add yticks as [runtime[0], runtime[1], runtime[2], ...]/3600
ax1.set_yticks(range(0, int(max(bottom_human) + 100), 500))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_human) + 100), 500)], fontsize=18)
ax2.set_yticks(range(0, int(max(bottom_primates) + 100), 500))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_primates) + 100), 500)], fontsize=18)

ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=19)
ax2.set_xlabel('Optimizations', fontsize=19)

# Adding a shared legend at the top
# fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.10), fontsize=12, ncol=6)
plt.tight_layout()
plt.savefig('combined_human_primates.pdf', bbox_inches='tight', format='pdf', dpi=1200)
