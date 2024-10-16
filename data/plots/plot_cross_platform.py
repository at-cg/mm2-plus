import matplotlib.pyplot as plt
import numpy as np

# Data for the architectures and datasets
architectures = ['Emerald Rapids', 'Sapphire Rapids', 'Cascade Lake', 'Milan']
datasets = ['(A) Barley-Barley', '(B) Maize-Maize', '(C) Human-Human', '(D) Human-Bonobo']

# Swapped runtime data for all architectures
runtime_base_SPR = [39813.224, 12698.36, 946.526, 1666.385]
runtime_opt_inter_SPR = [4446.136, 2894.757, 597.531, 861.231]

runtime_base_EMR = [37889.169, 12353.43, 911.475, 1565.657]
runtime_opt_inter_EMR = [4170.21, 2667.677, 568.826, 709.679]

runtime_base_Cascade = [0, 15707.519, 1135.649, 2247.109]
runtime_opt_inter_Cascade = [0, 3988.506, 741.815, 1211.59]

runtime_base_Milan = [34495.788, 11614.168, 979.621, 1703.788]
runtime_opt_inter_Milan = [5468.303, 2985.621, 743.411, 1040.442]

# Calculate speedup (base/inter)
speedup_SPR = np.array(runtime_base_SPR) / np.array(runtime_opt_inter_SPR)
speedup_EMR = np.array(runtime_base_EMR) / np.array(runtime_opt_inter_EMR)
speedup_Cascade = np.array(runtime_base_Cascade) / np.array(runtime_opt_inter_Cascade)
speedup_Milan = np.array(runtime_base_Milan) / np.array(runtime_opt_inter_Milan)

# Parameters for plotting
bar_width = 0.2  # Width of each bar
index = np.arange(len(datasets))  # X locations for datasets

# Creating the plot
fig, ax = plt.subplots(figsize=(8, 3))

# Plotting each architecture's speedup as grouped bars, ordered as EMR, SPR, Cascade, Milan
bars_EMR = ax.bar(index, speedup_EMR, bar_width, label='Emerald Rapids', zorder=3)
bars_SPR = ax.bar(index + bar_width, speedup_SPR, bar_width, label='Sapphire Rapids', zorder=3)
bars_Cascade = ax.bar(index + 2 * bar_width, speedup_Cascade, bar_width, label='Cascade Lake', zorder=3)
bars_Milan = ax.bar(index + 3 * bar_width, speedup_Milan, bar_width, label='Milan', zorder=3)

# Adding speedup labels on top of each bar
def add_labels(bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.1f}x',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 0.5),  # Offset label slightly above the bar
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=7, fontweight='bold')

# Add labels for each set of bars
add_labels(bars_EMR)
add_labels(bars_SPR)
add_labels(bars_Cascade)
add_labels(bars_Milan)

# Labeling the chart
ax.set_xlabel('Datasets', fontsize=10)
ax.set_ylabel('Speedup over minimap2', fontsize=10)
ax.set_xticks(index + 1.5 * bar_width)
ax.set_xticklabels(datasets, fontsize=10)
ax.legend(ncol=4, loc='upper center', fontsize=10, bbox_to_anchor=(0.5, 1.20))

# Grid and layout
ax.grid(axis='y', linestyle='--', zorder=0)
ax.set_ylim(0.0, 11.0)
plt.tight_layout()

# Saving the plot
plt.savefig('speedup_comparison_across_architectures.pdf', bbox_inches='tight', format='pdf', dpi=1200)