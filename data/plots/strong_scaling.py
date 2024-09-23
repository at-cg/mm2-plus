import matplotlib.pyplot as plt

# Provided data
threads = [8, 16, 32, 48]
human_human = [866.527, 744.970, 730.658, 725.438]
human_bonobo = [1422.528, 1202.867, 1172.766, 1081.117]
maize_maize = [5824.001, 3183.134, 2251.318, 2064.193]
barley_barley = [13616.107, 7618.431, 5981.484, 5883.384]

# Calculate speedup
def calculate_speedup(base_runtime, runtimes):
    return [base_runtime / rt for rt in runtimes]

human_human_speedup = calculate_speedup(human_human[0], human_human)
human_bonobo_speedup = calculate_speedup(human_bonobo[0], human_bonobo)
maize_maize_speedup = calculate_speedup(maize_maize[0], maize_maize)
barley_barley_speedup = calculate_speedup(barley_barley[0], barley_barley)

# Plotting with corrected aspect ratio and larger fonts
plt.figure(figsize=(10, 5))  # Adjust figure size

plt.plot(threads, human_bonobo_speedup, marker='o', label="Human-Bonobo")
plt.plot(threads, human_human_speedup, marker='o', label="Human-Human")
plt.plot(threads, maize_maize_speedup, marker='o', label="Maize-Maize")
plt.plot(threads, barley_barley_speedup, marker='o', label="Barley-Barley")

plt.xlabel("Threads", fontsize=14)
plt.ylabel("Speedup", fontsize=14)
plt.xticks(threads, fontsize=12)
plt.yticks(fontsize=12)
plt.legend(fontsize=12, reverse=True)
plt.grid(True)

# Save plot as PDF with high resolution
plt.savefig("strong_scaling.pdf", format="pdf", dpi=1200)
