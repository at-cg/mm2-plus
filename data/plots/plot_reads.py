import matplotlib.pyplot as plt
import numpy as np

# Corrected data for HiFi, ONT, and All-vs-All alignments (in hours)
runtimes_minimap2 = [2076.204 / 3600, 4061.623 / 3600, 1361.325 / 3600, 9529.873 / 3600, 21766.328 / 3600]
runtimes_mm2_plus = [1629.453 / 3600, 2575.712 / 3600, 977.766 / 3600, 4889.588 / 3600, 15763.013 / 3600]

# Titles for each subplot (swapped ONT UL and ONT Duplex)
titles = ['(A) HiFi', '(B) ONT Simplex', '(C) ONT Duplex', '(D) ONT Ultra-Long', '(E) ONT all-vs-all']

# Bar width and gap size
bar_width = 0.05
gap = 0.03

# Colors
colors = plt.get_cmap('tab10').colors

# Create a figure with 5 subplots
fig, axes = plt.subplots(1, 5, figsize=(14, 3.2))

# Plotting runtimes for each technology
for i, ax in enumerate(axes):
    # Plot minimap2 and mm2-plus runtimes
    ax.bar(- (bar_width + gap)/2, runtimes_minimap2[i], bar_width, color=colors[0], zorder=3)
    ax.bar((bar_width + gap)/2, runtimes_mm2_plus[i], bar_width, color=colors[1], zorder=3)
    
    # Adding runtime values
    ax.text(- (bar_width + gap)/2, runtimes_minimap2[i], f'{runtimes_minimap2[i]:.2f}h', ha='center', va='bottom', fontsize=12, fontweight='bold')
    ax.text((bar_width + gap)/2, runtimes_mm2_plus[i], f'{runtimes_mm2_plus[i]:.2f}h', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Formatting plot
    ax.set_xticks([- (bar_width + gap)/2, (bar_width + gap)/2])
    ax.set_xticklabels(['minimap2', 'mm2-plus'], rotation=0, fontsize=13)
    ax.set_title(titles[i], pad=15, fontsize=15)
    
    # Add grid lines
    ax.grid(axis='y', linestyle='--', zorder=0)

# Set Y-axis limits for each plot (customized based on the range of the data)
axes[0].set_ylim(0, 0.65)  # HiFi
axes[1].set_ylim(0, 1.27)  # ONT Simplex
axes[2].set_ylim(0, 0.43)  # ONT Duplex
axes[3].set_ylim(0, 3.0)  # ONT UL
axes[4].set_ylim(0, 6.8)  # ONT all-vs-all

# add axes[0] y label as runtime in hours
axes[0].set_ylabel('Runtime (hours)', fontsize=15)
#set fontsize=14 for yticks
axes[0].tick_params(axis='y', labelsize=14)
axes[1].tick_params(axis='y', labelsize=14)
axes[2].tick_params(axis='y', labelsize=14)
axes[3].tick_params(axis='y', labelsize=14)
axes[4].tick_params(axis='y', labelsize=14)

# Adjust the gap between subplots
plt.subplots_adjust(wspace=0.3)  # Increase the gap between the plots

# Adding common X-axis label
fig.supxlabel('Tools', fontsize=15)

# Adjust the layout
plt.tight_layout()

# Save the figure as PDF
plt.savefig('lr_ava.pdf', format='pdf', dpi=1200, bbox_inches='tight')