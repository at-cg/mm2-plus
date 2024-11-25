# Reproduce the results

## Overview
We provide scripts to reproduce the results. Please execute the following commands.

## Steps

### 1. Install and build the tools
#### Prerequisite
1. **GCC 9 or later** - [GCC](https://gcc.gnu.org/)
2. **Zlib** - [zlib](https://zlib.net/)
3. **Jemalloc** - [Jemalloc](https://github.com/jemalloc/jemalloc)

```bash
# Get the minimap2 v2.28 (with the profiling)
unzip minimap2_base.zip
git clone -b 'v1.0' --single-branch --depth 1 https://github.com/at-cg/mm2-plus.git
git clone -b 'v2.28' --single-branch --depth 1 https://github.com/lh3/minimap2
# build the tools
./make_exec.sh
```

### 2. Download the Datasets
Download the datasets for whole-genome and long-read alignment:
```bash
# Whole-genome datasets
# (A) Human-Human
cd human && ./get_fa.sh && cd ..
# (B) Human-Bonobo
cd primates && ./get_fa.sh && cd ..
# (C) Maize-Maize
cd maize && ./get_fa.sh && cd ..
# (D) Barley-Barley
cd barley && ./get_fa.sh && cd ..
```

### 3. Run the Tools
```bash
# Run the whole-genome alignment (base: minimap2, plus:mm2-plus)
# (A) Human-Human
./map_human-base.sh
./map_human-plus.sh

# (B) Human-Bonobo
./map_primates-base.sh
./map_primates-plus.sh

# (C) Maize-Maize
./map_maize-base.sh
./map_maize-plus.sh

# (D) Barley-Barley
./map_barley-base.sh
./map_barley-plus.sh
```

### 4. Compute the F1-score
```bash
# (A) Human-Human
cd human
./get_vcf.sh
./eval_vcf.sh

# (B) Human-Bonobo
cd primates
./get_vcf.sh
./eval_vcf.sh

# (C) Maize-Maize
cd maize
./get_vcf.sh
./eval_vcf.sh

# (D) Barley-Barley
cd barley
./get_vcf.sh
./eval_vcf.sh
```

<!-- ### 4. Get the anchor distribution
```bash
# build mm2-plus to write anchor_dist.txt and count_chains.txt
git clone -b 'v1.0' --single-branch --depth 1 https://github.com/at-cg/mm2-plus.git
cd mm2-plus && make all=1 get_dist=1 && cd .. # checkout the old commit

# (A) Human-Human
cd human
mm2-plus/minimap2 -t48 -x asm5 GCF_009914755.1_T2T-CHM13v2.0_genomic.fna GCA_018852605.2_Q100_hg002v1.0.1.pat_genomic.fna -o hap_anchor_dist.paf

# (A) Human-Bonobo
cd primates
mm2-plus/minimap2 -t48 -x asm20 GCF_009914755.1_T2T-CHM13v2.0_genomic.fna GCF_029289425.2_NHGRI_mPanPan1-v2.0_pri_genomic.fna -o hap_anchor_dist.paf

# (A) Maize-Maize
cd maize
mm2-plus/minimap2 -t48 -x asm5 Zm-Mo17-REFERENCE-CAU-2.0.fa Zm-W22-REFERENCE-NRGENE-2.0.fa -o hap_anchor_dist.paf

# (A) Barley-Barley
cd barley
mm2-plus/minimap2 -t48 -x asm5 Hordeum_vulgare.MorexV3_pseudomolecules_assembly.dna.toplevel.fa GCA_902500625.1_GPv1_genomic.fna -o hap_anchor_dist.paf
``` -->