#!/usr/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Consider errors in a pipeline

# Build minimap2-hap with avx + par_chain
cd mm2-plus && make deps  # Install dependencies
make clean && make profile=1 base=1 avx=1 opt_olp=1
cp mm2plus ../mm2plus_ao
make clean && make profile=1 base=1 avx=1 opt_olp=1 par_chain_1=1
cp mm2plus ../mm2plus_aoc1
make clean && make profile=1 base=1 avx=1 opt_olp=1 par_chain_1=1 par_btk=1
cp mm2plus ../mm2plus_aoc1b
make clean && make profile=1 base=1 avx=1 opt_olp=1 par_chain_1=1 par_btk=1 par_sort=1
cp mm2plus ../mm2plus_aoc1bs
cd ..

mkdir -p barley_mapped human_mapped primates_mapped maize_mapped
