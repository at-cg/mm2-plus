import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

plt.rcParams.update({'font.size': 12})  # Base font size scaled by 1.2

# Updated categories based on the mapping
categories = ['Computing anchors', 'Chaining (DP recursion)', 'Chaining (DP traceback)', 'Filtering primary chains', 'Base-to-base alignment', 'Miscellaneous']

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
runtime_primates = [2040.404, 1752.056, 1715.094, 1458.902, 1320.493, 1255.645]  # in seconds
value_mm2_primates = np.array([0.078, 0.256 + 0.123, 0.020 + 0.017, 0.012, 0.490, 0.005]) * runtime_primates[0]
value_mm2_avx_primates = np.array([0.084, 0.295 + 0.146, 0.022 + 0.019, 0.017, 0.412, 0.005]) * runtime_primates[1]
value_mm2_olp_primates = np.array([0.118, 0.305 + 0.148, 0.023 + 0.022, 0.000, 0.377, 0.007]) * runtime_primates[2]
value_mm2_hap_chain_primates = np.array([0.133, 0.175 + 0.143, 0.032 + 0.028, 0.000, 0.481, 0.008]) * runtime_primates[3]
value_mm2_hap_chain_btk_primates = np.array([0.106, 0.191 + 0.154, 0.012 + 0.010, 0.000, 0.518, 0.009]) * runtime_primates[4]
value_mm2_hap_chain_btk_sort_primates = np.array([0.089, 0.179 + 0.154, 0.015 + 0.012, 0.001, 0.547, 0.002]) * runtime_primates[5]
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
    ax1.text(i - 0.25, bottom_human[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=11)

# Plot bars for primates data
bottom_primates = np.zeros(len(runtime_primates))
for i, category in enumerate(categories):
    ax2.bar(range(len(runtime_primates)), data_primates[:, i], bottom=bottom_primates, color=colors[i], zorder=3)
    bottom_primates += data_primates[:, i]

# Add runtime labels for primates (in hours)
for i, v in enumerate(runtime_primates):
    ax2.text(i - 0.25, bottom_primates[i] + 50, f'{v/3600:.2f}h', color='black', fontweight='bold', fontsize=11)

# Set titles for both subplots
ax1.set_title('(C) Human-Human', fontsize=15, fontweight='bold')
ax2.set_title('(D) Human-Bonobo', fontsize=15, fontweight='bold')

# Set y-axis labels
ax1.set_ylabel('Runtime in hours', fontsize=15)
ax2.set_ylabel('  ', fontsize=15)

# Set x-tick labels for human and primates
ax1.set_xticks(range(len(runtime_human)))
ax1.set_xticklabels(['base', 'A', 'AO', 'AOC', 'AOBC', 'AOBCS'], rotation=0)

ax2.set_xticks(range(len(runtime_primates)))
ax2.set_xticklabels(['base', 'A', 'AO', 'AOC', 'AOBC', 'AOBCS'], rotation=0)

# Adjust y-limits to be non-normalized
ax1.set_ylim(0, max(bottom_human) + 200)
ax2.set_ylim(0, max(bottom_primates) + 200)

# Add yticks as runtime in hours
ax1.set_yticks(range(0, int(max(bottom_human) + 100), 500))
ax1.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_human) + 100), 500)])
ax2.set_yticks(range(0, int(max(bottom_primates) + 100), 500))
ax2.set_yticklabels([f'{i/3600:.1f}' for i in range(0, int(max(bottom_primates) + 100), 500)])

# Grid lines for y-axis
ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)

# Set xlabel for both subplots as 'Optimizations'
ax1.set_xlabel('Optimizations', fontsize=15)
ax2.set_xlabel('Optimizations', fontsize=15)

# Adding a shared legend at the top
fig.legend(categories, loc='upper center', bbox_to_anchor=(0.5, 1.10), fontsize=12, ncol=6)

plt.tight_layout()
plt.savefig('combined_human_primates_rt2.pdf', bbox_inches='tight', format='pdf', dpi=1200)
