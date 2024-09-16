import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Data for the pie charts
datasets = ['D_Human', 'D_Primates', 'D_Barley']

# Multiplying by 100 as specified
human  = np.array([0.091, 0.52, 0.046, 0.048, 0.289, 0.007]) * 100
primates = np.array([0.078, 0.379, 0.037, 0.012, 0.490, 0.005]) * 100
barley = np.array([0.027, 0.433, 0.085, 0.354, 0.089, 0.012]) * 100

# Combine the data into a list for easier iteration
data = [human, primates, barley]
titles = ['(A) Human-Human', '(B) Human-Bonobo', '(C) Barley-Barley']

# Use the 'tab10' color palette from seaborn
tab10_colors = sns.color_palette("tab10", len(human))

# Long category names for the legend
long_categories = [
    'Computing anchors', 'Chaining (DP recursion)', 'Chaining (DP traceback)', 'Filtering primary chains', 'Base-to-base alignment', 'Miscellaneous'
]

# Total runtimes for each dataset
runtimes = [1237.404, 2040.404, 42612.805]

# % CPU usage for each dataset
cpu_usages = [277, 303, 109]
# divide by 4800 and multiply by 100 to get the percentage
cpu_usages = [x/4800*100 for x in cpu_usages]

# Create a figure with 3 subplots (one for each dataset)
fig, axes = plt.subplots(1, 3, figsize=(16, 5))

# Custom function to display only significant values
def autopct_func(pct):
    return f'{pct:.1f}%' if pct > 5 else ''

# Loop over each dataset and create a pie chart
for i, ax in enumerate(axes):
    wedges, texts, autotexts = ax.pie(data[i], labels=None, autopct=autopct_func, 
                                      colors=tab10_colors, startangle=90, textprops=dict(color="w"),
                                      pctdistance=0.65)  # Shift value annotations outward
    ax.set_title(titles[i], fontsize=13)

    # Move value annotations outside the pie slices
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(11)
    
    # Add runtime at the bottom of each pie chart
    ax.text(0, -1.3, f'Runtime: {runtimes[i]/3600:.2f}h', ha='center', fontsize=13)
    
    # Add % CPU usage below the runtime
    ax.text(0, -1.5, f'CPU usage: {cpu_usages[i]:.2f}%', ha='center', fontsize=13)

# Add a single legend using the long category names
fig.legend(wedges, long_categories, loc='upper center', bbox_to_anchor=(0.5, 1.0), fontsize=10, ncol=6)

# Adjust the layout to make space for the legend and runtimes
plt.subplots_adjust(top=0.85, bottom=0.2)

# Save the plot to a consistent file name
plt.savefig("pie_charts_profile.pdf", format='pdf', dpi=1200, bbox_inches='tight')

# Show the plot (optional, if you're running this interactively)
plt.show()