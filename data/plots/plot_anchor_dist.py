import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# List of files and corresponding dataset names, reordered as requested
files = ['barley.txt', 'maize.txt', 'human.txt', 'primates.txt']
datasets = ['(A) Barley-Barley', '(B) Maize-Maize', '(C) Human-Human', '(D) Human-Bonobo']

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
fig, ax = plt.subplots(figsize=(7, 2.5))

# Create the box plot
ax.boxplot(data, showfliers=False, showmeans=False, meanline=False, 
           medianprops={'color':'lime', 'linewidth':2.2})

# Add data points to the plot
for i in range(len(data)):
    y = data[i]
    x = np.random.normal(i + 1, 0.04, size=len(y))  # Add some noise to the x-axis for better visualization
    ax.plot(x, y, 'r.', alpha=0.3, markersize=8)

# Set x-ticks and labels
ax.set_xticks(np.arange(1, len(datasets) + 1))
ax.set_xticklabels(datasets, rotation=0, fontsize=8)

# set yticks font size
plt.yticks(fontsize=8)

# Set labels for x-axis and y-axis
ax.set_xlabel("Datasets", fontsize=9)
ax.set_ylabel("Anchor fraction distribution", fontsize=9)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, 1.0)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("Anchor_distribution.pdf", bbox_inches='tight', dpi=1200, format='pdf')
