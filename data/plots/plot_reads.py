import matplotlib.pyplot as plt
import numpy as np

# Data for HiFi, ONT, and All-vs-All alignments (in hours)
runtimes_minimap2 = [4878.840 / 3600, 7364.320 / 3600, 27098.373 / 3600]
runtimes_mm2_plus = [2500.657 / 3600, 4487.814 / 3600, 16426.840 / 3600]

# Bar width and gap size
bar_width = 0.1
gap = 0.05

# Colors
colors = plt.get_cmap('tab10').colors

# Create a figure with 3 subplots
fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 3))

# Plotting HiFi alignment runtimes with a gap
bars_minimap2_hifi = ax1.bar(0 - (bar_width + gap)/2, runtimes_minimap2[0], bar_width, color=colors[0], zorder=3)
bars_mm2_plus_hifi = ax1.bar(0 + (bar_width + gap)/2, runtimes_mm2_plus[0], bar_width, color=colors[1], zorder=3)

# Adding runtime values for HiFi
ax1.text(0 - (bar_width + gap)/2, runtimes_minimap2[0], f'{runtimes_minimap2[0]:.2f}h', ha='center', va='bottom')
ax1.text(0 + (bar_width + gap)/2, runtimes_mm2_plus[0], f'{runtimes_mm2_plus[0]:.2f}h', ha='center', va='bottom')

# Formatting HiFi plot
ax1.set_xticks([0])
ax1.set_xticklabels(['PacBio HiFi'])
ax1.set_ylabel('Runtime (hours)')
ax1.set_title('(A) HG002_HiFi', pad=15)  # Adding gap between title and plot

# Plotting ONT alignment runtimes with a gap
bars_minimap2_ont = ax2.bar(0 - (bar_width + gap)/2, runtimes_minimap2[1], bar_width, color=colors[0], zorder=3)
bars_mm2_plus_ont = ax2.bar(0 + (bar_width + gap)/2, runtimes_mm2_plus[1], bar_width, color=colors[1], zorder=3)

# Adding runtime values for ONT
ax2.text(0 - (bar_width + gap)/2, runtimes_minimap2[1], f'{runtimes_minimap2[1]:.2f}h', ha='center', va='bottom')
ax2.text(0 + (bar_width + gap)/2, runtimes_mm2_plus[1], f'{runtimes_mm2_plus[1]:.2f}h', ha='center', va='bottom')

# Formatting ONT plot
ax2.set_xticks([0])
ax2.set_xticklabels(['ONT'])
ax2.set_ylabel(' ')
ax2.set_title('(B) HG002_ONT', pad=15)  # Adding gap between title and plot

# Plotting All-vs-All alignment runtimes with a gap
bars_minimap2_all = ax3.bar(0 - (bar_width + gap)/2, runtimes_minimap2[2], bar_width, color=colors[0], zorder=3)
bars_mm2_plus_all = ax3.bar(0 + (bar_width + gap)/2, runtimes_mm2_plus[2], bar_width, color=colors[1], zorder=3)

# Adding runtime values for All-vs-All
ax3.text(0 - (bar_width + gap)/2, runtimes_minimap2[2], f'{runtimes_minimap2[2]:.2f}h', ha='center', va='bottom')
ax3.text(0 + (bar_width + gap)/2, runtimes_mm2_plus[2], f'{runtimes_mm2_plus[2]:.2f}h', ha='center', va='bottom')

# Formatting All-vs-All plot
ax3.set_xticks([0])
ax3.set_xticklabels(['ONT'])
ax3.set_ylabel(' ')
ax3.set_title('(C) HG002_ONT_ava', pad=15)  # Adding gap between title and plot

# Add grid lines
ax1.grid(axis='y', linestyle='--', zorder=0)
ax2.grid(axis='y', linestyle='--', zorder=0)
ax3.grid(axis='y', linestyle='--', zorder=0)

# Set Y-axis limits
ax1.set_ylim(0, 1.50)
ax2.set_ylim(0, 2.30)
ax3.set_ylim(0, 8.3)

# Adding one common legend for all subplots
fig.legend(['minimap2', 'mm2-plus'], loc='upper right', bbox_to_anchor=(1.1, 0.85))

# Adding common X-axis label
fig.supxlabel('Long-read sequencing technology')

# Adjust the layout
plt.tight_layout()

# Save the figure as PDF
plt.savefig('lr_ava.pdf', format='pdf', dpi=1200, bbox_inches='tight')