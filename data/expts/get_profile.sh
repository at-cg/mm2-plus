#!/bin/bash

# Check if input is from a file or from stdin (pipe)
if [ "$1" == "-" ]; then
    input=$(cat)  # Read from stdin (pipe)
else
    input_file=$1

    # Check if the file exists
    if [ ! -f "$input_file" ]; then
        echo "File not found!"
        exit 1
    fi

    input=$(cat "$input_file")  # Read from the file
fi

# Extract fractions, runtime, and memory from the log data
echo "$input" | awk '
BEGIN {
    # Define the output array with zero-initialized values
    split("0 0 0 0 0 0 0 0", values)
}

/M::main.*Real time:/ {
    # Extract the runtime and memory usage
    match($0, /Real time: ([^;]+) sec; CPU: ([^;]+) sec; Peak RSS: ([^ ]+) GB/, stats)
    real_time = stats[1]
    cpu_time = stats[2]
    peak_rss = stats[3]
}

/M::main/ && /minimizer_lookup_frac:/ {
    # Extract the fractions using match and substr functions
    match($0, /minimizer_lookup_frac: ([^;]+); rmq_1_frac: ([^;]+); btk_1_frac: ([^;]+); rmq_2_frac: ([^;]+); btk_2_frac: ([^;]+); alignment_frac: ([^;]+); mm_set_frac: ([^;]+); other_frac: ([^;]+)/, fractions)

    # Map the fractions to the corresponding categories
    values[1] = fractions[1]  # Minimizer lookup
    values[2] = fractions[2]  # Chaining 1 (rmq_1)
    values[3] = fractions[3]  # Backtracking 1 (btk_1)
    values[4] = fractions[4]  # Chaining 2 (rmq_2)
    values[5] = fractions[5]  # Backtracking 2 (btk_2)
    values[6] = fractions[7]  # Overlap finding (mm_set)
    values[7] = fractions[6]  # Extension (alignment)
    values[8] = fractions[8]  # Miscellaneous (other)
}

END {
    # Print only the last set of values along with runtime and memory
    printf("Fractions: [%.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f, %.3f]\n", values[1], values[2], values[3], values[4], values[5], values[6], values[7], values[8])
    printf("Real time: %s sec\nCPU time: %s sec\nPeak RSS: %s GB\n", real_time, cpu_time, peak_rss)
}'
