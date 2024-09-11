import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 12})  # Base font size scaled by 1.2

# Data for the heatmap
short_categories = ['M', '$C_1$', '$B_1$', '$C_2$', '$B_2$', 'O', 'E', 'Ms']
datasets = ['D_Human', 'D_Primates', 'D_Barley']

# Multiplying by 100 as specified
human = np.array([0.091, 0.322, 0.025, 0.198, 0.021, 0.048, 0.289, 0.007]) * 100
primates = np.array([0.078, 0.256, 0.020, 0.123, 0.017, 0.012, 0.490, 0.005]) * 100
barley = np.array([0.027, 0.272, 0.044, 0.161, 0.041, 0.354, 0.089, 0.012]) * 100

# Combine the data into a 2D array
data = np.array([human, primates, barley])

# Create a heatmap with annotations formatted to 2 decimal places
plt.figure(figsize=(10, 4))
sns.heatmap(data, annot=True, fmt=".2f", cmap="Reds", xticklabels=short_categories, yticklabels=datasets)

# Add legends with full category names and an outer box using plt.figtext
legend_text = '''
M: Minimizer lookup
$C_1$: Chaining 1
$B_1$: Backtracking 1
$C_2$: Chaining 2
$B_2$: Backtracking 2
O: Overlap finding
E: Extension
Ms: Miscellaneous
'''

plt.figtext(0.95, 0.5, legend_text, fontsize=13, va='center')

# Adjust the layout to make space for the legend text
plt.subplots_adjust(right=0.75)  # Adjust space to the right to accommodate the legend box
plt.yticks(rotation=90)

# Call tight_layout to adjust the figure and make sure the elements are not clipped
plt.tight_layout()
plt.xlabel('Kernels', fontsize=14)
plt.ylabel('Datasets', fontsize=14)
# Save the plot to a PDF file with 'bbox_inches' set to 'tight'
plt.savefig("heat_map.pdf", format='pdf', dpi=1200, bbox_inches='tight')
