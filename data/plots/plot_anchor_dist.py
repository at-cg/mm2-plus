import numpy as np
import matplotlib.pyplot as plt

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

# Plot each dataset as points with jitter along the x-axis
for i in range(len(data)):
    y = data[i]
    x = np.full_like(y, i + 1) + np.random.normal(0, 0.04, size=len(y))  # Add some noise to x for better visualization
    ax.plot(x, y, 'r.', alpha=0.3, markersize=8)

# Set x-ticks and labels
ax.set_xticks(np.arange(1, len(datasets) + 1))
ax.set_xticklabels(datasets, rotation=0, fontsize=8)

# Set yticks font size
plt.yticks(fontsize=8)

# Set labels for x-axis and y-axis
ax.set_xlabel("Datasets", fontsize=9)
ax.set_ylabel("Maximum fraction of anchors \n on a single sequence", fontsize=9)

# Add a horizontal grid
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, 1.0)

# Adjust layout and save the figure
plt.tight_layout()
plt.savefig("Anchor_distribution.pdf", bbox_inches='tight', dpi=1200, format='pdf')