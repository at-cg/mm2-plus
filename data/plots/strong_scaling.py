#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# Data provided
threads = [8, 16, 32, 48]
human_human_mm2 = [866.527, 744.970, 730.658, 725.438]
human_bonobo_mm2 = [1465.370, 1358.687, 1215.547, 1182.213]
maize_maize_mm2 = [5824.001, 3183.134, 2251.318, 2064.193]
barley_barley_mm2 = [13616.107, 7618.431, 5981.484, 5883.384]

human_human_mm2_plus = [1140.774, 1124.689, 1125.017, 1126.743]
human_bonobo_mm2_plus = [1785.631, 1770.274, 1792.599, 1780.366]
maize_maize_mm2_plus = [13240.416, 13240.416, 13240.416, 13240.416]
barley_barley_mm2_plus = [42612.805, 42612.805, 42612.805, 42612.805]

# Convert runtimes from seconds to hours
def convert_to_hours(runtime_list):
    return [rt / 3600 for rt in runtime_list]

# Converting all runtime values to hours
human_human_mm2_hours = convert_to_hours(human_human_mm2)
human_bonobo_mm2_hours = convert_to_hours(human_bonobo_mm2)
maize_maize_mm2_hours = convert_to_hours(maize_maize_mm2)
barley_barley_mm2_hours = convert_to_hours(barley_barley_mm2)

human_human_mm2_plus_hours = convert_to_hours(human_human_mm2_plus)
human_bonobo_mm2_plus_hours = convert_to_hours(human_bonobo_mm2_plus)
maize_maize_mm2_plus_hours = convert_to_hours(maize_maize_mm2_plus)
barley_barley_mm2_plus_hours = convert_to_hours(barley_barley_mm2_plus)

# Create the horizontal arrangement of subplots
fig, axes = plt.subplots(1, 4, figsize=(12, 3))

# Function to set reduced yticks (starting Y-axis from 0) and make ticks uniform per plot with 2 decimal places
def set_uniform_yticks(ax):
    # Get maximum value of current plot for setting Y-axis ticks uniformly per plot
    max_val = ax.get_ylim()[1]
    yticks = np.linspace(0, max_val + 0.05, num=6)  # Create 6 evenly spaced ticks
    yticks = [round(y, 2) for y in yticks]  # Round ticks to 2 decimal places
    ax.set_ylim(bottom=0)  # Start Y-axis from 0
    ax.set_yticks(yticks)  # Set uniform ticks

# (A) Barley-Barley Runtime in hours
axes[0].plot(threads, barley_barley_mm2_plus_hours, marker='o', label='mm2-plus', color='tab:orange')
axes[0].plot(threads, barley_barley_mm2_hours, marker='o', label='minimap2', color='tab:blue')
axes[0].set_title('(A) Barley-Barley', fontsize=12)
axes[0].set_xlabel('Threads', fontsize=12)
axes[0].set_ylabel('Runtime (hours)', fontsize=12)
axes[0].set_xticks(threads)
set_uniform_yticks(axes[0])
axes[0].grid(linestyle='--', linewidth=0.5)

# (B) Maize-Maize Runtime in hours
axes[1].plot(threads, maize_maize_mm2_plus_hours, marker='o', label='mm2-plus', color='tab:orange')
axes[1].plot(threads, maize_maize_mm2_hours, marker='o', label='minimap2', color='tab:blue')
axes[1].set_title('(B) Maize-Maize', fontsize=12)
axes[1].set_xlabel('Threads', fontsize=12)
axes[1].set_xticks(threads)
set_uniform_yticks(axes[1])
axes[1].grid(linestyle='--', linewidth=0.5)

# (C) Human-Human Runtime in hours
axes[2].plot(threads, human_human_mm2_plus_hours, marker='o', label='mm2-plus', color='tab:orange')
axes[2].plot(threads, human_human_mm2_hours, marker='o', label='minimap2', color='tab:blue')
axes[2].set_title('(C) Human-Human', fontsize=12)
axes[2].set_xlabel('Threads', fontsize=12)
axes[2].set_xticks(threads)
set_uniform_yticks(axes[2])
axes[2].grid(linestyle='--', linewidth=0.5)

# (D) Human-Bonobo Runtime in hours
axes[3].plot(threads, human_bonobo_mm2_plus_hours, marker='o', label='mm2-plus', color='tab:orange')
axes[3].plot(threads, human_bonobo_mm2_hours, marker='o', label='minimap2', color='tab:blue')
axes[3].set_title('(D) Human-Bonobo', fontsize=12)
axes[3].set_xlabel('Threads', fontsize=12)
axes[3].set_xticks(threads)
set_uniform_yticks(axes[3])
axes[3].grid(linestyle='--', linewidth=0.5)

# Add a single legend at the top of the figure
fig.legend(['minimap2', 'mm2-plus'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.04))

plt.tight_layout(rect=[0, 0, 1, 0.95], w_pad=3)
plt.savefig("strong_scaling.pdf", format="pdf", dpi=1200, bbox_inches='tight')