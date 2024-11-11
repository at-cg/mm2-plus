import matplotlib.pyplot as plt
import numpy as np

# Corrected data for HiFi, ONT, and All-vs-All alignments (in hours)
runtimes_minimap2 = [0.58, 1.13, 0.38, 2.65, 6.05]
runtimes_mm2_fast = [0.48, 0.69, 0.26, 1.41, 4.49]
runtimes_mm2_plus = [0.44, 0.69, 0.26, 1.36, 4.38]

# Titles for each subplot (swapped ONT UL and ONT Duplex)
titles = ['(A) PacBio HiFi', '(B) ONT simplex', '(C) ONT duplex', '(D) ONT ultra-long', '(E) ONT all-vs-all']

# Bar width and gap size
bar_width = 0.05
gap = 0.03

# Colors
colors = plt.get_cmap('tab10').colors

# Create a figure with 5 subplots
fig, axes = plt.subplots(1, 5, figsize=(12, 3.4))

# Plotting runtimes for each technology
for i, ax in enumerate(axes):
    # Plot minimap2, mm2-fast, and mm2-plus runtimes
    ax.bar(- (bar_width + gap), runtimes_minimap2[i], bar_width, color=colors[0], zorder=3)
    ax.bar(0, runtimes_mm2_fast[i], bar_width, color=colors[2], zorder=3)
    ax.bar((bar_width + gap), runtimes_mm2_plus[i], bar_width, color=colors[1], zorder=3)
    
    # Adding runtime values
    ax.text(- (bar_width + gap), runtimes_minimap2[i], f'{runtimes_minimap2[i]:.2f}h', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text(0, runtimes_mm2_fast[i], f'{runtimes_mm2_fast[i]:.2f}h', ha='center', va='bottom', fontsize=10, fontweight='bold')
    ax.text((bar_width + gap), runtimes_mm2_plus[i], f'{runtimes_mm2_plus[i]:.2f}h', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Formatting plot
    ax.set_xticks([- (bar_width + gap), 0, (bar_width + gap)])
    ax.set_xticklabels(['minimap2', 'mm2-fast', 'mm2-plus'], rotation=90, fontsize=13)
    ax.set_title(titles[i], pad=10, fontsize=13)
    
    # Add grid lines
    ax.grid(axis='y', linestyle='--', zorder=0)

# Set Y-axis limits for each plot (customized based on the range of the data)
axes[0].set_ylim(0, 0.65)  # HiFi
axes[1].set_ylim(0, 1.27)  # ONT Simplex
axes[2].set_ylim(0, 0.43)  # ONT Duplex
axes[3].set_ylim(0, 3.0)   # ONT UL
axes[4].set_ylim(0, 6.8)   # ONT all-vs-all

# Add Y-axis label to the first subplot
axes[0].set_ylabel('Runtime (hours)', fontsize=13)

# Set fontsize=11 for y-tick labels on each subplot
for ax in axes:
    ax.tick_params(axis='y', labelsize=13)

# Adjust the gap between subplots
plt.subplots_adjust(wspace=0.4)  # Increased the gap between the plots

# Adding common X-axis label
fig.supxlabel('Tools', fontsize=13)

# Adjust the layout
plt.tight_layout()

# Save the figure as PDF
plt.savefig('lr_ava.pdf', format='pdf', dpi=1200, bbox_inches='tight')
