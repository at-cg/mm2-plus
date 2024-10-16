#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt

# Data
datasets = ['Barley-Barley', 'Maize-Maize', 'Human-Human', 'Human-Bonobo']
methods = ['Inter-chromosomal', 'Intra-chromosomal']
runtimes = [
    [5841.102, 6110.632],  # Barley-Barley
    [3380.453, 4006.088],  # Maize-Maize
    [727.938, 790.252],    # Human-Human
    [1174.683, 1386.812]   # Human-Bonobo
]

# Convert runtime in seconds to hours
def convert_to_hours(runtime_in_sec):
    return runtime_in_sec / 3600

# Plot settings
x = np.arange(len(methods))  # Label locations for methods
width = 0.35  # Width of the bars
gap = 0.15    # Gap between datasets

# Create the figure and axis
fig, ax = plt.subplots(figsize=(8, 3.5))

# Iterate through datasets and plot two bars (one for each method) with gaps between groups
bar_width = 0.4
gap = 1.2
bar_positions = []

# Generate bar positions for each dataset with a gap between them
for i in range(len(datasets)):
    pos = np.array([i * gap, i * gap + bar_width])
    bar_positions.append(pos)

# Plot bars and add text for runtime in hours on top of each bar
for i, (dataset_runtime, dataset_name) in enumerate(zip(runtimes, datasets)):
    # Convert to hours
    hours_runtime = [convert_to_hours(rt) for rt in dataset_runtime]
    
    # Plot bars for each method for the dataset and add legend only for the first dataset
    if i == 0:  # Add legend only for the first dataset
        bars = ax.bar(bar_positions[i], hours_runtime, bar_width, 
                      color=['tab:blue', 'tab:orange'], 
                      label=['Inter-chromosomal', 'Intra-chromosomal'], zorder=3)
    else:
        bars = ax.bar(bar_positions[i], hours_runtime, bar_width, color=['tab:blue', 'tab:orange'], zorder=3)
    
    # Add text on top of each bar
    for j, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height, f'{height:.2f}h', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Set xticks and labels for methods for each dataset
x_ticks = [(pos[0] + pos[1]) / 2 for pos in bar_positions]
ax.set_xticks(x_ticks)
ax.set_xticklabels(datasets, fontsize=12)

# set y ticks
ax.set_yticks(np.arange(0, 2.1, 0.5))

# Set axis labels and grid
ax.set_xlabel('Dataset', fontsize=12)
ax.set_ylabel('Runtime (hours)', fontsize=12)
ax.grid(axis='y')

# Adjust the legend to the upper left
ax.legend(loc='upper right', fontsize=10)

# Shorten the height of the plot
ax.set_ylim([0, 2.0])  # Adjusted y-axis to reduce height

# Display the plot
plt.tight_layout()
plt.savefig('inter_intra.pdf', format='pdf', dpi=1200)