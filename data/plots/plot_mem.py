#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt

# Data
datasets = ['Barley-Barley', 'Maize-Maize', 'Human-Human', 'Human-Bonobo']
methods = ['minimap2', 'mm2-plus']
memory_usage = [
    [220.768, 199.506],  # Barley-Barley
    [265.743, 196.085],  # Maize-Maize
    [29.969, 32.169],    # Human-Human
    [38.486, 41.663]     # Human-Bonobo
]

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

# Plot bars and add text for memory usage on top of each bar
for i, (dataset_memory, dataset_name) in enumerate(zip(memory_usage, datasets)):
    # Plot bars for each method for the dataset and add legend only for the first dataset
    if i == 0:  # Add legend only for the first dataset
        bars = ax.bar(bar_positions[i], dataset_memory, bar_width, 
                      color=['tab:blue', 'tab:orange'], 
                      label=['minimap2', 'mm2-plus'], zorder=3)
    else:
        bars = ax.bar(bar_positions[i], dataset_memory, bar_width, color=['tab:blue', 'tab:orange'], zorder=3)
    
    # Add text on top of each bar (rounded to 2 digits)
    for j, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2., height + 2, f'{height:.0f}GB', ha='center', va='bottom', fontsize=9, fontweight='bold')

# Set xticks and labels for methods for each dataset
x_ticks = [(pos[0] + pos[1]) / 2 for pos in bar_positions]
ax.set_xticks(x_ticks)
ax.set_xticklabels(datasets, fontsize=12)

# Set y ticks
ax.set_yticks(np.arange(0, 301, 50))

# Set axis labels and grid
ax.set_xlabel('Dataset', fontsize=12)
ax.set_ylabel('Memory Usage (GB)', fontsize=12)
ax.grid(axis='y')

# Adjust the legend to the upper right
ax.legend(loc='upper right', fontsize=10)

# Display the plot
plt.tight_layout()
plt.savefig('memory_usage.pdf', format='pdf', dpi=1200)