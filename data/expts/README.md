# Reproduce the results

## Overview
We provide scripts to reproduce the results. Please execute the following commands.

## Steps

### 1. Install and build the tools
#### Prerequisite
1. **GCC 9 or later** - [GCC](https://gcc.gnu.org/)
2. **Zlib** - [zlib](https://zlib.net/)
3. **Jemalloc** - [Jemalloc](https://github.com/jemalloc/jemalloc)
4. **SRA Toolkit** - [SRA Toolkit](https://github.com/ncbi/sra-tools)

```bash
# Get the minimap2 v2.28 (with the profiling)
gunzip minimap2_base.gz
git clone https://github.com/at-cg/mm2-plus.git
git clone https://github.com/lh3/minimap2
# build the tools
./make_exec.sh
cd minimap2 && make && cd ..
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

# Long-read datasets

# Create directory and get tools
mkdir -p Long-reads && cd Long-reads
git clone https://github.com/at-cg/mm2-plus.git
cd mm2-plus && git checkout dacaad1 && cd .. # checkout the old commit
git clone https://github.com/lh3/minimap2
cp -r mm2-plus mm2-fast
cd mm2-plus && make all=1 && cd ..
cd mm2-fast && make mm2_fast=1 && cd ..
cd minimap2 && make && cd ..

# Reference
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/009/914/755/GCF_009914755.1_T2T-CHM13v2.0/GCF_009914755.1_T2T-CHM13v2.0_genomic.fna.gz
gunzip GCF_009914755.1_T2T-CHM13v2.0_genomic.fna.gz

# HiFi
prefetch --max-size 512GB SRR26402938 && fasterq-dump --split-files ./SRR26402938/SRR26402938.sra

# ONT
prefetch --max-size 512GB SRR24678051 && fasterq-dump --split-files ./SRR24678051/SRR24678051.sra

# (A) ONT Duplex
prefetch --max-size 512GB SRR28295759 && fasterq-dump --split-files ./SRR28295759/SRR28295759.sra
prefetch --max-size 512GB SRR28295761 && fasterq-dump --split-files ./SRR28295761/SRR28295761.sra
prefetch --max-size 512GB SRR28295765 && fasterq-dump --split-files ./SRR28295765/SRR28295765.sra
prefetch --max-size 512GB SRR28295766 && fasterq-dump --split-files ./SRR28295766/SRR28295766.sra
prefetch --max-size 512GB SRR28295771 && fasterq-dump --split-files ./SRR28295771/SRR28295771.sra
cat SRR28295759.fastq SRR28295761.fastq SRR28295765.fastq SRR28295766.fastq SRR28295771.fastq > ONT_dup.fastq

# ONT Ultra-long
prefetch --max-size 512GB SRR24462105 && fasterq-dump --split-files ./SRR24462105/SRR24462105.sra
seqkit sample -p 0.1 SRR24462105.fastq -o SRR24462105_10p.fastq
```

### 3. Run the Tools
```bash
# Run the whole-genome alignment (base: minimap2, inter:inter-chromosomal chaining, intra: intra-chromosomal chaining )
# (A) Human-Human
./map_human-base.sh
./map_human-inter.sh
./map_human-inter.sh

# (A) Human-Bonobo
./map_primates-base.sh
./map_primates-inter.sh
./map_primates-inter.sh

# (A) Maize-Maize
./map_maize-base.sh
./map_maize-inter.sh
./map_maize-inter.sh

# (A) Barley-Barley
./map_barley-base.sh
./map_barley-inter.sh
./map_barley-inter.sh

# Run the long-reads alignment
cd Long-reads

# HiFi
minimap2/minimap2 -t48 -ax map-hifi GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR26402938.fastq > mm2_HiFi.paf
mm2-fast/minimap2 -t48 -ax map-hifi GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR26402938.fastq > mm2-fast_HiFi.paf
mm2-plus/minimap2 -t48 -ax map-hifi GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR26402938.fastq > mm2-plus_HiFi.paf

# ONT
minimap2/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24678051.fastq > mm2_ONT.paf
mm2-fast/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24678051.fastq > mm2-fast_ONT.paf
mm2-plus/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24678051.fastq > mm2-plus_ONT.paf

# ONT Duplex
minimap2/minimap2 -t48 -ax lr:hq GCF_009914755.1_T2T-CHM13v2.0_genomic.fna ONT_dup.fastq > mm2_ONT_dup.paf
mm2-fast/minimap2 -t48 -ax lr:hq GCF_009914755.1_T2T-CHM13v2.0_genomic.fna ONT_dup.fastq > mm2-fast_ONT_dup.paf
mm2-plus/minimap2 -t48 -ax lr:hq GCF_009914755.1_T2T-CHM13v2.0_genomic.fna ONT_dup.fastq > mm2-plus_ONT_dup.paf

# ONT Ultra-long
minimap2/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24462105_10p.fastq > mm2_ONT_ul.paf
mm2-fast/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24462105_10p.fastq > mm2-fast_ONT_ul.paf
mm2-plus/minimap2 -t48 -ax map-ont GCF_009914755.1_T2T-CHM13v2.0_genomic.fna SRR24462105_10p.fastq > mm2-plus_ONT_ul.paf

# ONT all-vs-all
minimap2/minimap2 -t48 -x ava-ont SRR24678051.fastq SRR24678051.fastq > mm2_ONT_ava.paf
mm2-fast/minimap2 -t48 -x ava-ont SRR24678051.fastq SRR24678051.fastq > mm2-fast_ONT_ava.paf
mm2-plus/minimap2 -t48 -x ava-ont SRR24678051.fastq SRR24678051.fastq > mm2-plus_ONT_ava.paf
```

### 4. Compute the F1-score
```bash
# (A) Human-Human
cd human
./get_vcf.sh
./eval_vcf.sh

# (A) Human-Bonobo
cd primates
./get_vcf.sh
./eval_vcf.sh

# (A) Maize-Maize
cd maize
./get_vcf.sh
./eval_vcf.sh

# (A) Barley-Barley
cd barley
./get_vcf.sh
./eval_vcf.sh
```

### 4. Get the anchor distribution
```bash
# build mm2-plus to write anchor_dist.txt
git clone https://github.com/at-cg/mm2-plus.git
cd mm2-plus && git checkout dacaad1 && make get_dist=1 && cd .. # checkout the old commit

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
```