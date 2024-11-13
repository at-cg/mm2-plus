#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

# Data provided (Swapped minimap2 and mm2-plus)
threads = [1, 2, 4, 8, 16, 32, 48]
xticks = ['1', '', '', '8', '16', '32', '48']
human_human_mm2_plus = [2761.216, 1616.403, 1140.444, 866.527, 744.970, 730.658, 725.438]
human_bonobo_mm2_plus = [5258.655, 3140.134, 1836.118, 1465.370, 1358.687, 1215.547, 1182.213]
maize_maize_mm2_plus = [24584.725, 15170.429, 9269.106, 6106.802, 4204.208, 3550.639, 3407.598]
barley_barley_mm2_plus = [32305.769, 19103.460, 11982.463, 7852.019, 6015.712, 5839.766, 5841.102]

human_human_mm2 = [2836.195, 1618.247, 1161.395, 1140.774, 1124.689, 1125.017, 1126.743]
human_bonobo_mm2 = [5581.250, 3295.056, 1951.608, 1785.631, 1770.274, 1792.599, 1780.366]
maize_maize_mm2 = [30311.550, 18282.159, 13200.353, 13161.858, 13174.924, 13200.120, 13128.412]
barley_barley_mm2 = [47567.911, 43037.359, 42764.748, 42612.805, 42612.805, 42612.805, 42612.805]

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

# Function to set 4 Y-axis ticks and format them to 2 decimal places
def set_yticks_count(ax, num_ticks):
    min_y, max_y = ax.get_ylim()
    yticks = np.linspace(min_y, max_y, num=num_ticks)
    ax.set_yticks(yticks)
    ax.set_yticklabels([f'{y:.1f}' for y in yticks])

# Plotting each subplot
datasets = [
    ('Barley-Barley', barley_barley_mm2_hours, barley_barley_mm2_plus_hours),
    ('Maize-Maize', maize_maize_mm2_hours, maize_maize_mm2_plus_hours),
    ('Human-Human', human_human_mm2_hours, human_human_mm2_plus_hours),
    ('Human-Bonobo', human_bonobo_mm2_hours, human_bonobo_mm2_plus_hours)
]

for i, (title, mm2_hours, mm2_plus_hours) in enumerate(datasets):
    axes[i].plot(threads, mm2_hours, marker='o', label='minimap2', color='tab:blue')
    axes[i].plot(threads, mm2_plus_hours, marker='o', label='mm2-plus', color='tab:orange')
    axes[i].set_title(f'({chr(65+i)}) {title}', fontsize=14)
    axes[i].set_xlabel('Threads', fontsize=15)
    axes[i].set_xticks(threads)
    axes[i].set_xticklabels(xticks, fontsize=13)
    axes[i].set_ylim(bottom=0)  # Ensure Y-axis starts at 0
    axes[i].grid(linestyle='--', linewidth=0.5)
    # set yticks font size to 12
    axes[i].tick_params(axis='y', labelsize=13)
    
    # Set 4 evenly spaced Y-axis ticks and format them to 2 decimal places
    set_yticks_count(axes[i], num_ticks=5)
    
    if i == 0:
        axes[i].set_ylabel('Runtime (hours)', fontsize=15)

# Add a single legend at the top of the figure
fig.legend(['minimap2', 'mm2-plus'], loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.10), fontsize=15)

plt.tight_layout(rect=[0, 0, 1, 0.95], w_pad=3)
plt.savefig("strong_scaling.pdf", format="pdf", dpi=1200, bbox_inches='tight')