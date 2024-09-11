import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams.update({'font.size': 7})  # Base font size scaled by 1.2

# List of files and corresponding dataset names
files = ['human.txt', 'primates.txt', 'maize.txt', 'barley.txt']
datasets = ['D_Human', 'D_Primates', 'D_Maize', 'D_Barley']

# Initialize an empty list to store the data
data = []

# Read data from each file and add it to the list
for file in files:
    with open(file, 'r') as f:
        values = [float(line.strip()) for line in f]
        data.append(values)

# Calculate and print the median values for each dataset
medians = [np.median(d) for d in data]
for dataset, median in zip(datasets, medians):
    print(f"Median for {dataset}: {median}")

# Create the figure and axis
fig, ax = plt.subplots(figsize=(5, 2))

# Create the box plot
ax.boxplot(data, showfliers=False, showmeans=False, meanline=False, 
           medianprops={'color':'lime', 'linewidth':2.2})

# Add data points to the plot
for i in range(len(data)):
    y = data[i]
    x = np.random.normal(i + 1, 0.04, size=len(y))  # Add some noise to the x-axis for better visualization
    ax.plot(x, y, 'r.', alpha=0.3, markersize=10)

# Set x-ticks and labels
ax.set_xticks(np.arange(1, len(datasets) + 1))
ax.set_xticklabels(datasets, rotation=0)

# Set labels for x-axis and y-axis
ax.set_xlabel("Datasets")
ax.set_ylabel("Anchor fraction distribution")
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, 1.0)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("Anchor_distribution.pdf", bbox_inches='tight', dpi=1200, format='pdf')
