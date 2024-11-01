#!/usr/bin/bash

# git clone https://github.com/gsc74/minimap2_base.git
# git clone https://github.com/gsc74/mm2-plus.git

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Consider errors in a pipeline

cd mm2-plus && git checkout dacaad1 && cd ..

# Build minimap2-hap with avx + par_chain
cd mm2-plus && make clean && make profile=1 avx=1 opt_olp=1
cp minimap2 ../minimap2_ao
make clean && make profile=1 avx=1 opt_olp=1 par_chain_1=1
cp minimap2 ../minimap2_aoc1
make clean && make profile=1 avx=1 opt_olp=1 par_chain_1=1 par_btk=1
cp minimap2 ../minimap2_aoc1b
make clean && make profile=1 avx=1 opt_olp=1 par_chain_1=1 par_btk=1 par_sort=1
cp minimap2 ../minimap2_aoc1bs
make clean && make profile=1 avx=1 opt_olp=1 par_chain_2=1
cp minimap2 ../minimap2_aoc2
make clean && make profile=1 avx=1 opt_olp=1 par_chain_2=1 par_btk=1
cp minimap2 ../minimap2_aoc2b
make clean && make profile=1 avx=1 opt_olp=1 par_chain_2=1 par_btk=1 par_sort=1
cp minimap2 ../minimap2_aoc2bs
cd ..

mkdir -p barley_mapped human_mapped primates_mapped maize_mapped
